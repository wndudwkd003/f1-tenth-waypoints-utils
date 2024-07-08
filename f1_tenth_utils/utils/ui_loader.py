import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import ament_index_python.packages


def load_ui():
    package_share_directory = ament_index_python.packages.get_package_share_directory('f1_tenth_utils')
    ui_file_path = os.path.join(package_share_directory, 'resource', 'ui', 'f1-tenth-utils-main.ui')

    window = QMainWindow()
    loadUi(ui_file_path, window)
    return window
