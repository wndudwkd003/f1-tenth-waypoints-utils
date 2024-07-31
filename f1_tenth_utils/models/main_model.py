import pandas as pd

class MainModel:
    def __init__(self):
        self._project_name = None
        self._relative_speed = None
        self._absolute_speed = None
        self._ml_click_print_coord = None
        self._ml_click_auto_input = None
        self._min_speed = None
        self._max_speed = None
        self._x = None
        self._y = None
        self._speed = None
        self._start = None
        self._dest = None
        self._number_of_nearby_waypoints = None
        self._nearby_waypoint_density = None
        self._select_waypoint_density = None
        self._increase_decrease = None
        self._current_change = None
        self._auto_backup = None
        self._backup_name = None
        self._selected_indexes = []
        self._map_file_content = None
        self._yaml_file_content = None
        self._csv_data = None
        self._map_file_path = None
        self._yaml_file_path = None
        self._csv_folder_path = None
        self._percentage_speed = None
        self._constant_speed = None

    def set_percentage_speed(self, percentage_speed):
        self._percentage_speed = percentage_speed

    def get_percentage_speed(self):
        return self._percentage_speed

    def set_constant_speed(self, constant_speed):
        self._constant_speed = constant_speed

    def get_constant_speed(self):
        return self._constant_speed

    def set_map_file_content(self, content):
        self._map_file_content = content

    def get_map_file_content(self):
        return self._map_file_content

    def set_yaml_file_content(self, content):
        self._yaml_file_content = content

    def get_yaml_file_content(self):
        return self._yaml_file_content

    def set_csv_data(self, data):
        self._csv_data = data

    def get_csv_data(self):
        return self._csv_data

    def set_map_file_path(self, path):
        self._map_file_path = path

    def get_map_file_path(self):
        return self._map_file_path

    def set_yaml_file_path(self, path):
        self._yaml_file_path = path

    def get_yaml_file_path(self):
        return self._yaml_file_path

    def set_csv_folder_path(self, path):
        self._csv_folder_path = path

    def get_csv_folder_path(self):
        return self._csv_folder_path

    def set_selected_indexes(self, indexes):
        self._selected_indexes = indexes

    def get_selected_indexes(self):
        return self._selected_indexes

    def set_project_name(self, name):
        self._project_name = name

    def get_project_name(self):
        return self._project_name

    def set_relative_speed(self, value):
        self._relative_speed = value

    def get_relative_speed(self):
        return self._relative_speed

    def set_absolute_speed(self, value):
        self._absolute_speed = value

    def get_absolute_speed(self):
        return self._absolute_speed

    def set_ml_click_print_coord(self, value):
        self._ml_click_print_coord = value

    def get_ml_click_print_coord(self):
        return self._ml_click_print_coord

    def set_ml_click_auto_input(self, value):
        self._ml_click_auto_input = value

    def get_ml_click_auto_input(self):
        return self._ml_click_auto_input

    def set_min_speed(self, speed):
        self._min_speed = speed

    def get_min_speed(self):
        return self._min_speed

    def set_max_speed(self, speed):
        self._max_speed = speed

    def get_max_speed(self):
        return self._max_speed

    def set_x(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_speed(self, speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

    def set_start(self, start):
        self._start = start

    def get_start(self):
        return self._start

    def set_dest(self, dest):
        self._dest = dest

    def get_dest(self):
        return self._dest

    def set_number_of_nearby_waypoints(self, num):
        self._number_of_nearby_waypoints = num

    def get_number_of_nearby_waypoints(self):
        return self._number_of_nearby_waypoints

    def set_nearby_waypoint_density(self, density):
        self._nearby_waypoint_density = density

    def get_nearby_waypoint_density(self):
        return self._nearby_waypoint_density

    def set_select_waypoint_density(self, density):
        self._select_waypoint_density = density

    def get_select_waypoint_density(self):
        return self._select_waypoint_density

    def set_increase_decrease(self, inc_dec):
        self._increase_decrease = inc_dec

    def get_increase_decrease(self):
        return self._increase_decrease

    def set_current_change(self, change):
        self._current_change = change

    def get_current_change(self):
        return self._current_change

    def set_auto_backup(self, auto_backup):
        self._auto_backup = auto_backup

    def get_auto_backup(self):
        return self._auto_backup

    def set_backup_name(self, name):
        self._backup_name = name

    def get_backup_name(self):
        return self._backup_name
