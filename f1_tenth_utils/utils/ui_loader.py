import os
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.uic import loadUi
from ..static.ProjectManager import ProjectManager
import ament_index_python.packages

def load_ui():
    package_share_directory = ament_index_python.packages.get_package_share_directory('f1_tenth_utils')

    # Project Manager 싱글톤에 src 폴더의 경로를 저장해놓음
    pm = ProjectManager()
    pm.src_code_path = os.path.abspath(
        os.path.join(package_share_directory, os.pardir, os.pardir, os.pardir, os.pardir, 'src', 'f1_tenth_utils'))
    pm.projects_path = os.path.join(pm.src_code_path, 'f1_tenth_utils', 'projects')


    ui_file_path = os.path.join(package_share_directory, 'resource', 'ui', 'f1_tenth_utils_main.ui')
    window = QMainWindow()
    loadUi(ui_file_path, window)
    return window

def load_speed_dialog():
    try:
        package_share_directory = ament_index_python.packages.get_package_share_directory('f1_tenth_utils')
        ui_file_path = os.path.join(package_share_directory, 'resource', 'ui', 'f1_tenth_utils_dialog_speed.ui')
        dialog = QDialog()
        loadUi(ui_file_path, dialog)
        print(f"Loaded UI from {ui_file_path}")
        return dialog
    except Exception as e:
        print(f"Failed to load UI: {e}")
        return None