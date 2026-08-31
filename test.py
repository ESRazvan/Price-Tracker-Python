import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                            QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
                            QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal

#create one widget with vbox layout to contain a label and a button, the widget constitutes a cell inside gridlayout of settings dash
def vbox_cell_widget(label_text: str, button_text: str, parent = None) -> QWidget:
    cell_container = QWidget(parent, objectName = "grid_cell")
    cell_layout = QVBoxLayout(cell_container)

    button = QPushButton(button_text, cell_container)
    label = QLabel(label_text, cell_container)

    cell_layout.addWidget(button)
    cell_layout.addWidget(label)

    cell_container.setFixedHeight(100)

    return cell_container

class SidebarWidget(QFrame):
    #set custom signals so that mainwindow class can serve as the interface between sidebar and content area, separating them
    tracker_btn_clicked = pyqtSignal()
    settings_btn_clicked = pyqtSignal()

    def __init__(self, parent = None) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.setObjectName("SidebarWidget")

        self.tracker_btn = QPushButton("test1", self)
        self.settings_btn = QPushButton("test2", self)

        self.sidebar_label = QLabel("Price Tracker App", self)

        layout.addWidget(self.sidebar_label, alignment = Qt.AlignHCenter)
        layout.addWidget(self.tracker_btn, alignment = Qt.AlignHCenter)
        layout.addWidget(self.settings_btn, alignment = Qt.AlignHCenter)
        layout.addStretch()

        self.setFixedWidth(225)

        self.tracker_btn.clicked.connect(self.tracker_btn_clicked.emit)
        self.settings_btn.clicked.connect(self.settings_btn_clicked.emit)

class PriceTrackerDashboard(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.setObjectName("PriceTrackerWidget")

        self.test_label = QLabel("Caine", self)

        layout.addWidget(self.test_label)

class SettingsDashboard(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__()
        grid_layout = QGridLayout(self)

        #make one qhboxlayout with a label and a button inside and then add it to the grid as a cell.
        cell1 = vbox_cell_widget("apasa", "aici", self)
        cell2 = vbox_cell_widget("apasa", "aici", self)

        grid_layout.addWidget(cell1, 0, 0)
        grid_layout.addWidget(cell2, 0, 1)

#stacked widget to display only one widget
class ContentArea(QStackedWidget):
    def __init__(self, parent = None, *args : QWidget) -> None:
        super().__init__()
        for widget in args:
            self.addWidget(widget)
        #self.addWidget(args[0])
        #self.addWidget(args[1])

    def widget_select(self, widget : QWidget) -> None:
        self.setCurrentWidget(widget)

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
        self.settings_dash = SettingsDashboard()
        self.content_area = ContentArea(None, self.price_tracker_dash, self.settings_dash)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)
        main_layout.setStretchFactor(self.content_area, 1)

        #when the signal is emitted from sidebar button the widget select function of content area is called
        #with the specific widget object that we want to display as a parameter(lambda is needed so the function isnt called instantly)
        self.sidebar.tracker_btn_clicked.connect(lambda: self.content_area.widget_select(self.price_tracker_dash))
        self.sidebar.settings_btn_clicked.connect(lambda: self. content_area.widget_select(self.settings_dash))

        self.setCentralWidget(central_container)

def main() -> None:
    app = QApplication([])

    #initialize styles globally from an external qss file
    with open ("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    main_window = PriceTrackerApp()
    main_window.show()

    sys.exit(app.exec_())

main()