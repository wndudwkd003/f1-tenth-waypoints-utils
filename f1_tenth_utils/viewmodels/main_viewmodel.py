from PyQt5.QtCore import QObject, pyqtSlot

class MainViewModel(QObject):
    def __init__(self, model, view):
        super().__init__()
        self._model = model
        self._view = view

    @pyqtSlot()
    def new_project(self):
        project_name = self._view.get_project_name()
        if project_name:
            self._model.set_project_name(project_name)
            self._view.set_project_name(project_name)

    @pyqtSlot()
    def map_window_clicked(self):
        print("pbtn_map_window 이거를 클릭함")

    @pyqtSlot(str)
    def min_speed_changed(self, value):
        self._model.set_min_speed(value)
        print(f"Minimum speed: {value}")