import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                            QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout)
from PyQt5.QtCore import Qt

def vbox_cell_widget(label_text: str, button_text: str, parent = None) -> QWidget:
    cell_container = QWidget(parent)
    cell_layout = QVBoxLayout(cell_container)

    button = QPushButton(button_text, cell_container)
    label = QLabel(label_text, cell_container)

    cell_layout.addWidget(button)
    cell_layout.addWidget(label)

    cell_container.setFixedHeight(100)
    cell_container.setStyleSheet("""
    
    """)

    return cell_container

class SidebarWidget(QFrame):
    def __init__(self, parent = None) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
    
        self.tracker_btn = QPushButton("test1", self)
        self.settings_btn = QPushButton("test2", self)

        self.sidebar_label = QLabel("Price Tracker App", self)

        layout.addWidget(self.sidebar_label, alignment = Qt.AlignHCenter)
        layout.addWidget(self.tracker_btn, alignment = Qt.AlignHCenter)
        layout.addWidget(self.settings_btn, alignment = Qt.AlignHCenter)
        layout.addStretch()

        self.setFixedWidth(225)
        self.setStyleSheet("""
        QFrame { 
            border-right: 2px solid #000000; 
            background-color: transparent;
        }

        QPushButton {
            padding: 15px 75px;
            margin: 10px;
            border: 1px solid #000000;
            background-color: transparent;
        }

        QLabel { 
            font-size: 20px;
            color: #000000; 
            border: none;
            margin-bottom: 50px;
        }
        """)

class PriceTrackerDashboard(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.test_label = QLabel("Caine", self)

        layout.addWidget(self.test_label)

class SettingsDashboard(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__()
        grid_layout = QGridLayout(self)

        #make one qhboxlayout with a label and a button inside and then add it to the grid as a cell.
        """cell1 = vbox_cell_widget("apasa", "aici", self)
        cell2 = vbox_cell_widget("apasa", "aici", self)


        grid_layout.addWidget(cell1, 0, 0)
        grid_layout.addWidget(cell2, 0, 1)"""




class PriceTrackerApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        available_screen_size = QApplication.primaryScreen().availableGeometry()
        window_size = (available_screen_size.width() // 2, available_screen_size.height() // 2)

        #centering the initial position of the window on the screen
        window_init_position = tuple(map(lambda x : x // 2, window_size))
        self.setGeometry(*window_init_position, *window_size)

        self.initUI()


    def initUI(self) -> None:
        self.setWindowTitle("Price Tracker App")

        central_container = QWidget()
        main_layout = QHBoxLayout(central_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = SidebarWidget()
        self.price_tracker_dash = PriceTrackerDashboard()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.price_tracker_dash)
        main_layout.setStretchFactor(self.price_tracker_dash, 1)

        """self.settings_dash = SettingsDashboard()
        main_layout.addWidget(self.settings_dash)
        main_layout.setStretchFactor(self.settings_dash, 1)"""

        

        self.setCentralWidget(central_container)


def main() -> None:
    app = QApplication([])
    main_window = PriceTrackerApp()
    main_window.show()
    sys.exit(app.exec_())

main()