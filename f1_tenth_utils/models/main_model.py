class MainModel:
    def __init__(self):
        self._project_name = ""
        self._min_speed = ""

    def set_project_name(self, name):
        self._project_name = name

    def get_project_name(self):
        return self._project_name

    def set_min_speed(self, speed):
        self._min_speed = speed

    def get_min_speed(self):
        return self._min_speed