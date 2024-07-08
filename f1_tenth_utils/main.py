import sys
from PyQt5.QtWidgets import QApplication
from f1_tenth_utils.utils.ui_loader import load_ui
from f1_tenth_utils.views.main.main_view import MainView
from f1_tenth_utils.viewmodels.main_viewmodel import MainViewModel
from f1_tenth_utils.models.main_model import MainModel
import rclpy

def main(args=None):
    rclpy.init(args=args)
    app = QApplication(sys.argv)

    # UI 로드
    ui_window = load_ui()

    # MVVM 컴포넌트 초기화
    model = MainModel()
    view = MainView(ui_window)
    viewmodel = MainViewModel(model, view)

    # 뷰와 뷰모델 연결
    view.setup_connections(viewmodel)

    ui_window.show()
    sys.exit(app.exec_())
    rclpy.shutdown()

if __name__ == "__main__":
    main()