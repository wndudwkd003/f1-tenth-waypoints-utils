import os
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from f1_tenth_utils.static.ProjectManager import ProjectManager
from f1_tenth_utils.utils.csv_index_helper import copy_csv_files, load_csv_file
import shutil


class MainViewModel(QObject):
    def __init__(self, model, view):
        super().__init__()
        self._model = model
        self._view = view
        self.pm = ProjectManager()

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

        tree = ET.ElementTree(root)
        tree.write(f1tp_file_path, encoding='utf-8', xml_declaration=True)
        print(f"Project directory and files created: {project_dir}")
        return f1tp_file_path

    def load_xml_to_model_and_view(self, file_name):
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()
            project_name = root.find('Name').text
            relative_speed = root.find('RelativeSpeed').text == "true"
            absolute_speed = root.find('AbsoluteSpeed').text == "true"
            ml_click_print_coord = root.find('MLCLickPrintCoord').text == "true"
            ml_click_auto_input = root.find('MLCLickAutoInput').text == "true"
            min_speed = root.find('MinSpeed').text
            max_speed = root.find('MaxSpeed').text
            x = root.find('X').text
            y = root.find('Y').text
            speed = root.find('Speed').text
            start = root.find('Start').text
            dest = root.find('Dest').text
            number_of_nearby_waypoints = root.find('NumberOfNearbyWaypoints').text
            nearby_waypoint_density = root.find('NearbyWaypointDensity').text
            select_waypoint_density = root.find('SelectWaypointDensity').text
            increase_decrease = root.find('IncreaseDecrease').text
            current_change = root.find('CurrentChange').text
            auto_backup = root.find('AutoBackup').text == "true"
            backup_name = root.find('BackupName').text

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

            print(f"Loaded project: {project_name}")

            # CSV 파일 로드
            csv_dir = os.path.join(self.pm.projects_path, project_name, 'fundamental', 'csv')
            lane_optimal_path = os.path.join(csv_dir, 'lane_optimal.csv')
            if os.path.exists(lane_optimal_path):
                self.load_csv_to_table(lane_optimal_path)

        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Failed to load project: {e}')

    def load_csv_to_table(self, csv_path):
        csv_data = load_csv_file(csv_path)
        self._view.clear_table()  # 기존 테이블 내용 지우기
        for row in csv_data:
            self._view.add_table_row(row[0], row[1], row[2])
        print(f"{os.path.basename(csv_path)} loaded into table")

    @pyqtSlot()
    def new_project(self):
        project_name = self._view.get_project_name()
        if project_name:
            self._model.set_project_name(project_name)

            project_dir = os.path.join(self.pm.projects_path, project_name)

            if os.path.exists(project_dir):
                QMessageBox.warning(None, 'Warning', 'Project with the same name already exists.')
            else:
                try:
                    os.makedirs(project_dir)
                    os.makedirs(os.path.join(project_dir, 'fundamental'))
                    os.makedirs(os.path.join(project_dir, 'backup'))

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

                    # 모델 값을 XML에 저장하고 파일 경로를 반환
                    f1tp_file_path = self.save_model_to_xml(project_dir, project_name)

                    # UI에 설정
                    self.load_xml_to_model_and_view(f1tp_file_path)

                except Exception as e:
                    print(f"Failed to create project directory: {e}")

    @pyqtSlot()
    def load_project(self):
        file_name = self._view.load_project()
        if file_name:
            self.load_xml_to_model_and_view(file_name)

    @pyqtSlot()
    def load_map(self):
        files = self._view.load_map()
        if files:
            map_file, yaml_file = files
            print(f"Map file loaded: {map_file}")
            print(f"YAML file loaded: {yaml_file}")

            # 맵 파일과 YAML 파일을 프로젝트 디렉토리의 fundamental/map 폴더로 복사
            project_dir = os.path.join(self.pm.projects_path, self._model.get_project_name())
            map_dir = os.path.join(project_dir, 'fundamental', 'map')
            os.makedirs(map_dir, exist_ok=True)
            try:
                shutil.copy(map_file, map_dir)
                shutil.copy(yaml_file, map_dir)
                print(f"Map and YAML files copied to: {map_dir}")

                # 맵 파일을 모델에 저장
                self._model.set_map_file_path(map_file)
                self._view.display_map(map_file)  # 맵 파일 화면에 표시
            except Exception as e:
                QMessageBox.warning(None, 'Error', f'Failed to copy map or YAML file: {e}')

    @pyqtSlot()
    def load_csv(self):
        folder_name = self._view.load_csv()
        if folder_name:
            try:
                project_dir = os.path.join(self.pm.projects_path, self._model.get_project_name())
                csv_dir = os.path.join(project_dir, 'fundamental', 'csv')

                copy_csv_files(folder_name, csv_dir)
                print(f"CSV files copied to: {csv_dir}")

                # lane_optimal.csv 파일 읽기 및 QTableWidget에 추가
                lane_optimal_path = os.path.join(csv_dir, 'lane_optimal.csv')
                if os.path.exists(lane_optimal_path):
                    self.load_csv_to_table(lane_optimal_path)

            except Exception as e:
                QMessageBox.warning(None, 'Error', f'Failed to copy CSV files: {e}')

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
