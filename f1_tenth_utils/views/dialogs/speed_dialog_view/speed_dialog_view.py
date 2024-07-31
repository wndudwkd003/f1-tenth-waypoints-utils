from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from f1_tenth_utils.utils.ui_loader import load_speed_dialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

class SpeedDialogView(QDialog):
    def __init__(self, model=None):
        super(SpeedDialogView, self).__init__()
        self.ui = load_speed_dialog()
        self.setWindowTitle("Speed Change Dialog")
        self.model = model

        # Check if the widget exists
        if hasattr(self.ui, 'w_speed_current'):
            print("w_speed_current widget found.")
        else:
            print("w_speed_current widget not found.")
            return

        if hasattr(self.ui, 'w_speed_preview'):
            print("w_speed_preview widget found.")
        else:
            print("w_speed_preview widget not found.")
            return

        # 그래프를 그릴 수 있도록 설정
        self.figure_current = Figure()
        self.canvas_current = FigureCanvas(self.figure_current)
        self.toolbar_current = NavigationToolbar(self.canvas_current, self)

        self.figure_preview = Figure()
        self.canvas_preview = FigureCanvas(self.figure_preview)
        self.toolbar_preview = NavigationToolbar(self.canvas_preview, self)

        # Create layout if not present
        if not self.ui.w_speed_current.layout():
            layout = QVBoxLayout(self.ui.w_speed_current)
            self.ui.w_speed_current.setLayout(layout)
        else:
            layout = self.ui.w_speed_current.layout()
        layout.addWidget(self.toolbar_current)
        layout.addWidget(self.canvas_current)

        if not self.ui.w_speed_preview.layout():
            layout = QVBoxLayout(self.ui.w_speed_preview)
            self.ui.w_speed_preview.setLayout(layout)
        else:
            layout = self.ui.w_speed_preview.layout()
        layout.addWidget(self.toolbar_preview)
        layout.addWidget(self.canvas_preview)

        print("Canvas added to layout.")

        # Connect signals and slots here
        self.ui.up_button.clicked.connect(self.on_up_button_clicked)
        self.ui.down_button.clicked.connect(self.on_down_button_clicked)
        self.ui.preview_button.clicked.connect(self.on_preview_button_clicked)

        print("SpeedDialogView initialized successfully.")

        self.plot_selected_indexes()
        self.new_speed_data = []

    def on_up_button_clicked(self):
        print("Up button clicked")
        self.adjust_current_change(0.5)

    def on_down_button_clicked(self):
        print("Down button clicked")
        self.adjust_current_change(-0.5)

    def adjust_current_change(self, delta):
        try:
            current_value = float(self.ui.current_change_text.toPlainText())
        except ValueError:
            current_value = 0.0
        new_value = current_value + delta
        self.ui.current_change_text.setPlainText(f"{new_value:.2f}")

    def plot_selected_indexes(self, speed_data=None, plot_preview=False):
        selected_indexes = self.model.get_selected_indexes()
        print(f"Selected indexes: {selected_indexes}")
        if not selected_indexes:
            QMessageBox.warning(self, "Warning", "Please select at least one waypoint.")
            return

        csv_data = self.model.get_csv_data()
        if csv_data is None:
            QMessageBox.warning(self, "Warning", "CSV data is not loaded.")
            return

        print(f"CSV data head: {csv_data.head()}")

        if speed_data is None:
            speed_data = []
            try:
                for index in selected_indexes:
                    if index < len(csv_data):
                        row = csv_data.iloc[index]
                        print(f"Accessing row {index}: {row}")
                        speed = float(row[2])
                        speed_data.append(speed)
                        print(f"Row data - index: {index}, speed: {speed}")
                    else:
                        print(f"Index {index} out of range for csv_data")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to plot data: {e}")
                print(f"Failed to plot data: {e}")

        if plot_preview:
            self.figure_preview.clear()
            ax = self.figure_preview.add_subplot(111)
            canvas = self.canvas_preview
        else:
            self.figure_current.clear()
            ax = self.figure_current.add_subplot(111)
            canvas = self.canvas_current

        ax.plot([i + 1 for i in selected_indexes], speed_data, 'o-')
        ax.set_xlabel('Index')
        ax.set_ylabel('Speed')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # x축을 정수 단위로 설정
        canvas.draw()
        print("Plotting completed successfully.")

    def on_preview_button_clicked(self):
        try:
            increase_decrease_value = float(self.ui.current_change_text.toPlainText())  # 사용자가 입력한 값을 가져옴
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter a valid number for increase/decrease value.")
            return

        selected_indexes = self.model.get_selected_indexes()
        csv_data = self.model.get_csv_data()
        if not selected_indexes or csv_data is None:
            QMessageBox.warning(self, "Warning", "Please select at least one waypoint and ensure CSV data is loaded.")
            return

        original_speeds = [float(csv_data.iloc[i, 2]) for i in selected_indexes if i < len(csv_data)]
        new_speeds = []

        if self.model.get_percentage_speed():
            new_speeds = [s * (1 + increase_decrease_value / 100.0) for s in original_speeds]
        elif self.model.get_constant_speed():
            new_speeds = [s + increase_decrease_value for s in original_speeds]

        original_speed_avg = sum(original_speeds) / len(original_speeds) if original_speeds else 0
        new_speed_avg = sum(new_speeds) / len(new_speeds) if new_speeds else 0
        percentage_change = (
                    (new_speed_avg - original_speed_avg) / original_speed_avg * 100) if original_speed_avg != 0 else 0

        # 증감률을 표시하는 텍스트 박스 업데이트
        self.ui.inc_dec_text.setPlainText(f"{percentage_change:.2f}%")

        # 미리보기 그래프를 그리는 부분
        self.plot_selected_indexes(new_speeds, plot_preview=True)

    def exec_(self):
        self.ui.exec_()
