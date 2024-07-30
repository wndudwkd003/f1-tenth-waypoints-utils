import os.path

from PyQt5.QtWidgets import QMainWindow, QInputDialog, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QColor, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

class MainView(QMainWindow):
    def __init__(self, ui_window):
        super().__init__()
        self.ui = ui_window
        self.map_canvas = None

    def setup_connections(self, viewmodel):
        # Action project
        self.ui.actionNew_Project.triggered.connect(viewmodel.new_project)
        self.ui.actionLoad_Project.triggered.connect(viewmodel.load_project)

        # Action Load
        self.ui.actionLoad_Map.triggered.connect(viewmodel.load_map)
        self.ui.actionLoad_CSV.triggered.connect(viewmodel.load_csv)

        # ETC
        self.ui.pbtn_map_window.clicked.connect(viewmodel.map_window_clicked)
        self.ui.le_min_speed.textChanged.connect(viewmodel.min_speed_changed)
        self.ui.le_max_speed.textChanged.connect(viewmodel.max_speed_changed)
        self.ui.pbtn_select_waypoint.clicked.connect(viewmodel.select_waypoint)

    def get_project_name(self):
        project_name, ok = QInputDialog.getText(self, 'New Project', 'Enter project name:')
        return project_name if ok else None

    def load_project(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Project", "",
                                                   "F1 Tenth Project Files (*.f1tp);;All Files (*)", options=options)
        return file_name

    def load_map(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Load Map", "",
                                                    "Map Files (*.pgm *.png *.yaml);;All Files (*)", options=options)
        if files:
            # 파일 확장자 검증
            valid_extensions = {'.pgm', '.png', '.yaml'}
            selected_files = [file for file in files if os.path.splitext(file)[1].lower() in valid_extensions]

            if len(selected_files) != 2:
                QMessageBox.warning(self, 'Invalid Selection', 'Please select exactly two files: one map file (.pgm or .png) and one YAML file.')
                return None

            map_files = set()
            yaml_files = set()

            for file in selected_files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in {'.pgm', '.png'}:
                    map_files.add(file)
                elif file_extension == '.yaml':
                    yaml_files.add(file)

            if len(map_files) != 1 or len(yaml_files) != 1:
                QMessageBox.warning(self, 'Invalid Selection',
                                    'Please select one map file (.pgm or .png) and one YAML file.')
                return None

            return map_files.pop(), yaml_files.pop()

    def load_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_name = QFileDialog.getExistingDirectory(self, "Load CSV Folder", "", options=options)
        return folder_name

    def set_project_name(self, name):
        self.ui.label_current_project_name.setText(f"Current Project : {name}")

    def set_relative_speed(self, value):
        self.ui.rb_reltv_speed.setChecked(value)

    def set_absolute_speed(self, value):
        self.ui.rb_abs_speed.setChecked(value)

    def set_ml_click_print_coord(self, value):
        self.ui.cb_ml_print_coord.setChecked(value)

    def set_ml_click_auto_input(self, value):
        self.ui.cb_auto_input.setChecked(value)

    def set_min_speed(self, speed):
        self.ui.le_min_speed.setText(speed)

    def set_max_speed(self, speed):
        self.ui.le_max_speed.setText(speed)

    def set_x(self, x):
        self.ui.le_add_waypoint_x.setText(x)

    def set_y(self, y):
        self.ui.le_add_waypoint_y.setText(y)

    def set_speed(self, speed):
        self.ui.le_add_waypoint_speed.setText(speed)

    def set_start(self, start):
        self.ui.le_select_start_idx.setText(start)

    def set_dest(self, dest):
        self.ui.le_select_dest_idx.setText(dest)

    def set_number_of_nearby_waypoints(self, num):
        self.ui.le_nearby_wapoint_count.setText(num)

    def set_nearby_waypoint_density(self, density):
        self.ui.le_nearby_wapoint_density.setText(density)

    def set_select_waypoint_density(self, density):
        self.ui.le_nearby_selected_wapoint_density.setText(density)

    def set_increase_decrease(self, inc_dec):
        self.ui.le_inc_dec.setText(inc_dec)

    def set_current_change(self, change):
        self.ui.le_current_change.setText(change)

    def set_auto_backup(self, auto_backup):
        self.ui.cb_auto_backup.setChecked(auto_backup)

    def set_backup_name(self, name):
        self.ui.le_backup_name.setText(name)

    def clear_table(self):
        self.ui.tw_selected_waypoints.setRowCount(0)
        self.ui.tw_selected_waypoints.setHorizontalHeaderLabels(['X', 'Y', 'Speed'])

    def add_table_row(self, x, y, speed):
        row_position = self.ui.tw_selected_waypoints.rowCount()
        self.ui.tw_selected_waypoints.insertRow(row_position)
        self.ui.tw_selected_waypoints.setItem(row_position, 0, QTableWidgetItem(str(x)))
        self.ui.tw_selected_waypoints.setItem(row_position, 1, QTableWidgetItem(str(y)))
        self.ui.tw_selected_waypoints.setItem(row_position, 2, QTableWidgetItem(str(speed)))

    def highlight_table_range(self, indexes):
        for row in indexes:
            for col in range(self.ui.tw_selected_waypoints.columnCount()):
                item = self.ui.tw_selected_waypoints.item(row, col)
                if item:
                    item.setForeground(QBrush(QColor("red")))

    def clear_table_range_highlight(self, indexes):
        for row in indexes:
            for col in range(self.ui.tw_selected_waypoints.columnCount()):
                item = self.ui.tw_selected_waypoints.item(row, col)
                if item:
                    item.setForeground(QBrush(QColor("black")))


    def display_map(self, map_path):
        if hasattr(self, 'map_canvas') and self.map_canvas is not None:
            # 기존의 캔버스가 있다면 제거
            layout = self.ui.w_map.layout()
            if layout:
                layout.removeWidget(self.map_canvas)
                self.map_canvas.deleteLater()
            self.map_canvas = None

        # 새로운 캔버스 생성
        fig = Figure()
        self.map_canvas = FigureCanvas(fig)

