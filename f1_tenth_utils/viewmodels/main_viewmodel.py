import os
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QDialog
from f1_tenth_utils.static.ProjectManager import ProjectManager
from f1_tenth_utils.utils.csv_index_helper import copy_csv_files, load_csv_file
import shutil
from f1_tenth_utils.utils.utilities import Utilities
from f1_tenth_utils.views.dialogs.speed_dialog_view.speed_dialog_view import SpeedDialogView
import yaml
import pandas as pd
from PyQt5.QtGui import QPixmap


def get_text_or_default(element, default=''):
    return element.text if element is not None else default


class MainViewModel(QObject):
    def __init__(self, model, view):
        super().__init__()
        self._model = model
        self._view = view
        self._pm = ProjectManager()

    def save_model_to_xml(self, project_dir, project_name):
        # .f1tp 파일 생성
        f1tp_file_path = os.path.join(project_dir, f'{project_name}.f1tp')
        root = ET.Element("Project")

        ET.SubElement(root, "Name").text = self._model.get_project_name()
        ET.SubElement(root, "RelativeSpeed").text = str(self._model.get_relative_speed()).lower()
        ET.SubElement(root, "AbsoluteSpeed").text = str(self._model.get_absolute_speed()).lower()
        ET.SubElement(root, "MLCLickPrintCoord").text = str(self._model.get_ml_click_print_coord()).lower()
        ET.SubElement(root, "MLCLickAutoInput").text = str(self._model.get_ml_click_auto_input()).lower()
        ET.SubElement(root, "MinSpeed").text = self._model.get_min_speed()
        ET.SubElement(root, "MaxSpeed").text = self._model.get_max_speed()
        ET.SubElement(root, "X").text = self._model.get_x()
        ET.SubElement(root, "Y").text = self._model.get_y()
        ET.SubElement(root, "Speed").text = self._model.get_speed()
        ET.SubElement(root, "Start").text = self._model.get_start()
        ET.SubElement(root, "Dest").text = self._model.get_dest()
        ET.SubElement(root, "NumberOfNearbyWaypoints").text = self._model.get_number_of_nearby_waypoints()
        ET.SubElement(root, "NearbyWaypointDensity").text = self._model.get_nearby_waypoint_density()
        ET.SubElement(root, "SelectWaypointDensity").text = self._model.get_select_waypoint_density()
        ET.SubElement(root, "IncreaseDecrease").text = self._model.get_increase_decrease()
        ET.SubElement(root, "CurrentChange").text = self._model.get_current_change()
        ET.SubElement(root, "AutoBackup").text = str(self._model.get_auto_backup()).lower()
        ET.SubElement(root, "BackupName").text = self._model.get_backup_name()
        ET.SubElement(root, "MapFilePath").text = self._model.get_map_file_path()
        ET.SubElement(root, "YamlFilePath").text = self._model.get_yaml_file_path()
        ET.SubElement(root, "CsvFolderPath").text = self._model.get_csv_folder_path()
        ET.SubElement(root, "PercentageSpeed").text = str(self._model.get_percentage_speed()).lower()
        ET.SubElement(root, "ConstantSpeed").text = str(self._model.get_constant_speed()).lower()

        tree = ET.ElementTree(root)
        tree.write(f1tp_file_path, encoding='utf-8', xml_declaration=True)
        print(f"Project directory and files created: {project_dir}")
        return f1tp_file_path

    def load_xml_to_model_and_view(self, file_name):
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()

            project_name = get_text_or_default(root.find('Name'))
            relative_speed = get_text_or_default(root.find('RelativeSpeed'), 'false') == "true"
            absolute_speed = get_text_or_default(root.find('AbsoluteSpeed'), 'false') == "true"
            ml_click_print_coord = get_text_or_default(root.find('MLCLickPrintCoord'), 'false') == "true"
            ml_click_auto_input = get_text_or_default(root.find('MLCLickAutoInput'), 'false') == "true"
            min_speed = get_text_or_default(root.find('MinSpeed'), '3.0')
            max_speed = get_text_or_default(root.find('MaxSpeed'), '8.5')
            x = get_text_or_default(root.find('X'), '0.0')
            y = get_text_or_default(root.find('Y'), '0.0')
            speed = get_text_or_default(root.find('Speed'), '0.0')
            start = get_text_or_default(root.find('Start'), '0')
            dest = get_text_or_default(root.find('Dest'), '0')
            number_of_nearby_waypoints = get_text_or_default(root.find('NumberOfNearbyWaypoints'), '0')
            nearby_waypoint_density = get_text_or_default(root.find('NearbyWaypointDensity'), '0.1')
            select_waypoint_density = get_text_or_default(root.find('SelectWaypointDensity'), '1.0')
            increase_decrease = get_text_or_default(root.find('IncreaseDecrease'), '0.0')
            current_change = get_text_or_default(root.find('CurrentChange'), '0.1')
            auto_backup = get_text_or_default(root.find('AutoBackup'), 'false') == "true"
            backup_name = get_text_or_default(root.find('BackupName'), 'backup')
            map_file_path = get_text_or_default(root.find('MapFilePath'))
            yaml_file_path = get_text_or_default(root.find('YamlFilePath'))
            csv_folder_path = get_text_or_default(root.find('CsvFolderPath'))
            percentage_speed = get_text_or_default(root.find('PercentageSpeed'), 'false') == "true"
            constant_speed = get_text_or_default(root.find('ConstantSpeed'), 'true') == "true"

            # 모델에 저장
            self._model.set_project_name(project_name)
            self._model.set_relative_speed(relative_speed)
            self._model.set_absolute_speed(absolute_speed)
            self._model.set_ml_click_print_coord(ml_click_print_coord)
            self._model.set_ml_click_auto_input(ml_click_auto_input)
            self._model.set_min_speed(min_speed)
            self._model.set_max_speed(max_speed)
            self._model.set_x(x)
            self._model.set_y(y)
            self._model.set_speed(speed)
            self._model.set_start(start)
            self._model.set_dest(dest)
            self._model.set_number_of_nearby_waypoints(number_of_nearby_waypoints)
            self._model.set_nearby_waypoint_density(nearby_waypoint_density)
            self._model.set_select_waypoint_density(select_waypoint_density)
            self._model.set_increase_decrease(increase_decrease)
            self._model.set_current_change(current_change)
            self._model.set_auto_backup(auto_backup)
            self._model.set_backup_name(backup_name)
            self._model.set_map_file_path(map_file_path)
            self._model.set_yaml_file_path(yaml_file_path)
            self._model.set_csv_folder_path(csv_folder_path)
            self._model.set_percentage_speed(percentage_speed)
            self._model.set_constant_speed(constant_speed)

            # UI에 설정
            self._view.set_project_name(project_name)
            self._view.set_relative_speed(relative_speed)
            self._view.set_absolute_speed(absolute_speed)
            self._view.set_ml_click_print_coord(ml_click_print_coord)
            self._view.set_ml_click_auto_input(ml_click_auto_input)
            self._view.set_min_speed(min_speed)
            self._view.set_max_speed(max_speed)
            self._view.set_x(x)
            self._view.set_y(y)
            self._view.set_speed(speed)
            self._view.set_start(start)
            self._view.set_dest(dest)
            self._view.set_number_of_nearby_waypoints(number_of_nearby_waypoints)
            self._view.set_nearby_waypoint_density(nearby_waypoint_density)
            self._view.set_select_waypoint_density(select_waypoint_density)
            self._view.set_increase_decrease(increase_decrease)
            self._view.set_current_change(current_change)
            self._view.set_auto_backup(auto_backup)
            self._view.set_backup_name(backup_name)
            self._view.set_percentage_speed(percentage_speed)
            self._view.set_constant_speed(constant_speed)

            # 파일 내용을 모델에 저장
            if map_file_path and os.path.exists(map_file_path):
                with open(map_file_path, 'rb') as file:
                    self._model.set_map_file_content(file.read())
                self._view.display_map(map_file_path)

            if yaml_file_path and os.path.exists(yaml_file_path):
                with open(yaml_file_path, 'r') as file:
                    self._model.set_yaml_file_content(yaml.safe_load(file))

            if csv_folder_path and os.path.exists(csv_folder_path):
                lane_optimal_path = os.path.join(csv_folder_path, 'lane_optimal.csv')
                if os.path.exists(lane_optimal_path):
                    self.load_csv_to_table(lane_optimal_path)

            print(f"Loaded project: {project_name}")

        except Exception as e:
            Utilities.show_warning_message('Error', f'Failed to load project: {e}', e)

    def load_csv_to_table(self, csv_path):
        csv_data = pd.read_csv(csv_path, header=None)
        self._model.set_csv_data(csv_data)
        self._view.clear_table()  # 기존 테이블 내용 지우기
        for index, row in csv_data.iterrows():
            self._view.add_table_row(row[0], row[1], row[2])
        print(f"{os.path.basename(csv_path)} loaded into table")

    @pyqtSlot()
    def save_project(self):
        project_name = self._model.get_project_name()
        project_dir = os.path.join(self._pm.projects_path, project_name)

        if not project_name:
            QMessageBox.warning(None, 'Error', 'Project name is invalid.')
            return

        try:
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
                os.makedirs(os.path.join(project_dir, 'fundamental'))
                os.makedirs(os.path.join(project_dir, 'backup'))

            # 모델 값을 XML에 저장하고 파일 경로를 반환
            f1tp_file_path = self.save_model_to_xml(project_dir, project_name)
            self._pm.f1tp_file_path = f1tp_file_path
            self._pm.project_path = project_dir
            print(f"Project saved: {project_name}")

            # 맵 파일 및 YAML 파일 저장
            map_file_content = self._model.get_map_file_content()
            yaml_file_content = self._model.get_yaml_file_content()
            if map_file_content:
                map_dir = os.path.join(project_dir, 'fundamental', 'map')
                os.makedirs(map_dir, exist_ok=True)  # 필요한 디렉토리 생성
                map_file_path = os.path.join(map_dir, 'map.pgm')
                with open(map_file_path, 'wb') as file:
                    file.write(map_file_content)
                print(f"Map file saved to: {map_file_path}")

            if yaml_file_content:
                map_dir = os.path.join(project_dir, 'fundamental', 'map')
                os.makedirs(map_dir, exist_ok=True)  # 필요한 디렉토리 생성
                yaml_file_path = os.path.join(map_dir, 'map.yaml')
                with open(yaml_file_path, 'w') as file:
                    yaml.dump(yaml_file_content, file)
                print(f"YAML file saved to: {yaml_file_path}")

            # CSV 파일 저장
            csv_data = self._model.get_csv_data()
            if csv_data is not None:
                csv_dir = os.path.join(project_dir, 'fundamental', 'csv')
                os.makedirs(csv_dir, exist_ok=True)
                csv_file_path = os.path.join(csv_dir, 'lane_optimal.csv')
                csv_data.to_csv(csv_file_path, index=False)
                print(f"CSV file saved to: {csv_file_path}")

        except Exception as e:
            Utilities.show_warning_message('Error', 'Failed to save project', e)

    @pyqtSlot()
    def new_project(self):
        project_name = self._view.get_project_name()
        if project_name:
            self._model.set_project_name(project_name)

            tmp_project_dir = os.path.join(self._pm.projects_path, '.tmp', project_name)
            if os.path.exists(tmp_project_dir):
                shutil.rmtree(tmp_project_dir)  # 기존 임시 디렉토리 제거
            os.makedirs(tmp_project_dir, exist_ok=True)
            os.makedirs(os.path.join(tmp_project_dir, 'fundamental'), exist_ok=True)
            os.makedirs(os.path.join(tmp_project_dir, 'backup'), exist_ok=True)

            # 모델에 기본값 설정
            self._model.set_relative_speed(False)
            self._model.set_absolute_speed(True)
            self._model.set_ml_click_print_coord(False)
            self._model.set_ml_click_auto_input(False)
            self._model.set_min_speed("3.0")
            self._model.set_max_speed("8.5")
            self._model.set_x("0.0")
            self._model.set_y("0.0")
            self._model.set_speed("0.0")
            self._model.set_start("0")
            self._model.set_dest("0")
            self._model.set_number_of_nearby_waypoints("0")
            self._model.set_nearby_waypoint_density("0.1")
            self._model.set_select_waypoint_density("1.0")
            self._model.set_increase_decrease("0.0")
            self._model.set_current_change("0.1")
            self._model.set_auto_backup(False)
            self._model.set_backup_name("backup")

            # UI에 설정
            self._view.set_project_name(project_name)
            self._view.set_relative_speed(False)
            self._view.set_absolute_speed(True)
            self._view.set_ml_click_print_coord(False)
            self._view.set_ml_click_auto_input(False)
            self._view.set_min_speed("3.0")
            self._view.set_max_speed("8.5")
            self._view.set_x("0.0")
            self._view.set_y("0.0")
            self._view.set_speed("0.0")
            self._view.set_start("0")
            self._view.set_dest("0")
            self._view.set_number_of_nearby_waypoints("0")
            self._view.set_nearby_waypoint_density("0.1")
            self._view.set_select_waypoint_density("1.0")
            self._view.set_increase_decrease("0.0")
            self._view.set_current_change("0.1")
            self._view.set_auto_backup(False)
            self._view.set_backup_name("backup")

            # 작업 디렉토리 설정
            self._pm.project_path = tmp_project_dir
            print(f"Temporary project created: {project_name} in {tmp_project_dir}")

    @pyqtSlot()
    def load_project(self):
        file_name = self._view.load_project()
        if file_name:
            project_name = os.path.splitext(os.path.basename(file_name))[0]
            project_dir = os.path.join(self._pm.projects_path, project_name)

            # 프로젝트 로드
            self.load_xml_to_model_and_view(file_name)

            # 작업 디렉토리 설정
            self._pm.project_path = project_dir
            print(f"Loaded project: {project_name} from {project_dir}")

    @pyqtSlot()
    def load_map(self):
        files = self._view.load_map()
        if files:
            map_file, yaml_file = files
            print(f"Map file loaded: {map_file}")
            print(f"YAML file loaded: {yaml_file}")

            # 맵 파일 경로와 내용을 모델에 저장
            with open(map_file, 'rb') as file:
                self._model.set_map_file_content(file.read())
            self._model.set_map_file_path(map_file)

            with open(yaml_file, 'r') as file:
                self._model.set_yaml_file_content(yaml.safe_load(file))
            self._model.set_yaml_file_path(yaml_file)

            # 기존 위젯 제거
            for i in reversed(range(self._view.ui.w_map.layout().count())):
                widget = self._view.ui.w_map.layout().itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # 새 레이아웃 설정
            self.display_map(map_file)

    def display_map(self, map_file):
        # 이미지 파일을 QPixmap으로 로드
        pixmap = QPixmap(map_file)

        # QGraphicsScene과 QGraphicsView 생성
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        view = QGraphicsView(scene)

        # QVBoxLayout을 사용하여 QGraphicsView를 w_map에 추가
        layout = QVBoxLayout()
        layout.addWidget(view)

        # 기존 레이아웃을 제거하고 새로운 레이아웃을 추가
        for i in reversed(range(self._view.ui.w_map.layout().count())):
            widget = self._view.ui.w_map.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self._view.ui.w_map.setLayout(layout)

        # 맵의 크기에 맞게 격자 조정
        view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    @pyqtSlot()
    def load_csv(self):
        folder_name = self._view.load_csv()
        if folder_name:
            try:
                self._model.set_csv_folder_path(folder_name)
                lane_optimal_path = os.path.join(folder_name, 'lane_optimal.csv')
                if os.path.exists(lane_optimal_path):
                    csv_data = pd.read_csv(lane_optimal_path)
                    self._model.set_csv_data(csv_data)
                    self.load_csv_to_table(lane_optimal_path)
                    print(f"CSV folder path set to: {folder_name}")
            except Exception as e:
                Utilities.show_warning_message('Error', f'Failed to load CSV files: {e}', e)

    @pyqtSlot()
    def select_waypoint(self):
        start_idx = int(self._view.ui.le_select_start_idx.text()) - 1  # 1을 빼서 0부터 시작하도록 조정
        dest_idx = int(self._view.ui.le_select_dest_idx.text()) - 1  # 1을 빼서 0부터 시작하도록 조정

        if start_idx > dest_idx:
            QMessageBox.warning(None, 'Error', 'Start index cannot be greater than Dest index.')
            return

        total_rows = self._view.ui.tw_selected_waypoints.rowCount()
        if start_idx < 0 or dest_idx >= total_rows:
            QMessageBox.warning(None, 'Error', 'Selected range is out of bounds.')
            return

        # 이전 선택 해제
        old_selected_indexes = self._model.get_selected_indexes()
        self._view.clear_table_range_highlight(old_selected_indexes)

        # 새로운 선택 적용
        selected_indexes = list(range(start_idx, dest_idx + 1))
        self._model.set_selected_indexes(selected_indexes)

        # 새로운 선택 강조 표시
        self._view.highlight_table_range(selected_indexes)
        print(f"Waypoints from index {start_idx + 1} to {dest_idx + 1} added.")  # 출력 시에는 다시 1을 더해서 사용자에게 표시

    @pyqtSlot()
    def map_window_clicked(self):
        print("pbtn_map_window 이거를 클릭함")

    @pyqtSlot(str)
    def min_speed_changed(self, value):
        self._model.set_min_speed(value)
        print(f"Minimum speed: {value}")

    @pyqtSlot(str)
    def max_speed_changed(self, value):
        self._model.set_max_speed(value)
        print(f"Maximum speed: {value}")

    @pyqtSlot()
    def show_speed_dialog(self):
        selected_indexes = self._model.get_selected_indexes()
        if not selected_indexes:
            QMessageBox.warning(None, "Warning", "Please select at least one waypoint.")
            return

        dialog = SpeedDialogView(self._model)
        dialog.exec_()

    @pyqtSlot(bool)
    def percentage_speed_changed(self, checked):
        if checked:
            self._model.set_percentage_speed(True)
            self._model.set_constant_speed(False)
            print("Percentage speed selected.")

    @pyqtSlot(bool)
    def constant_speed_changed(self, checked):
        if checked:
            self._model.set_percentage_speed(False)
            self._model.set_constant_speed(True)
            print("Constant speed selected.")
