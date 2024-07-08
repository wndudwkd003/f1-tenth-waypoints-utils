from PyQt5.QtWidgets import QMainWindow, QInputDialog
from PyQt5.uic import loadUi

class MainView(QMainWindow):
    def __init__(self, ui_window):
        super().__init__()
        self.ui = ui_window

    def setup_connections(self, viewmodel):
        self.ui.actionNew_Project.triggered.connect(viewmodel.new_project)
        self.ui.pbtn_map_window.clicked.connect(viewmodel.map_window_clicked)
        self.ui.le_min_speed.textChanged.connect(viewmodel.min_speed_changed)

    def get_project_name(self):
        project_name, ok = QInputDialog.getText(self, 'New Project', 'Enter project name:')
        return project_name if ok else None

    def set_project_name(self, name):
        self.ui.label_current_project_name.setText(f"Current Project : {name}")

    def get_min_speed(self):
        return self.ui.le_min_speed.text()