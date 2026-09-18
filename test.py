import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
                             QStackedWidget, QCheckBox)
from PyQt5.QtCore import (Qt, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve,
                          pyqtProperty)
from PyQt5.QtGui import QPainter, QColor

#create one widget with vbox layout to contain a label and a button, the widget constitutes a cell inside gridlayout of settings dash
def vbox_cell_widget(label_text: str, parent = None) -> QWidget:
    cell_container = QWidget(parent, objectName = "grid_cell")
    cell_layout = QVBoxLayout(cell_container)

    button = ToggleButton(cell_container)
    label = QLabel(label_text, cell_container)

    cell_layout.addWidget(label)
    cell_layout.addWidget(button)

    cell_container.setFixedHeight(100)

    return cell_container

#Custom toggle button built on top of existing checkbox widget
class ToggleButton(QCheckBox):
    def __init__(self, parent = None, title = None) -> None:
        super().__init__()
        self.setFixedSize(60, 30)
        self.text = title

        #initial unchecked position of circle
        #putting _ before a variable name is a convention that shows this variable is protected inside a class
        self._x_pos = 15

        #handle animation logic
        self.clicked.connect(self.button_clicked)

        #button colors
        self.outline_color = "#3F4047"
        self.unchecked_color = "#2F3036"
        self.checked_color = "#93E1D8"

        #animation speficic variables
        self.easing_curve = QEasingCurve.OutSine
        self.animation_duration = 300 #ms

    #Override the hitbutton function to set the clickable area of the button as the whole rect that it occupies
    def hitButton(self, pos):
        return self.rect().contains(pos)

    #define a getter for the x coordinate position to be able to animate it
    #using a @pyqtProperty() decorator registers the property inside of qt's internal c++ engine
    @pyqtProperty(int)
    def xPos(self) -> int:
        return self._x_pos

    @xPos.setter
    def xPos(self, value) -> None:
        if self._x_pos != value:
            self._x_pos = value
            self.update()

    def button_clicked(self) -> None:
        if self.checkState() == False:
            self.check_to_uncheck()
        else:
            self.uncheck_to_check()

    def uncheck_to_check(self) -> None:
            self.animation = QPropertyAnimation(self, b'xPos') #(object which holds this property, property name)
            self.animation.setDuration(self.animation_duration)
            self.animation.setStartValue(self.xPos)
            self.animation.setEndValue(self.width() - 15)
            self.animation.setEasingCurve(self.easing_curve)
            self.animation.start()

    def check_to_uncheck(self) -> None:
            self.animation = QPropertyAnimation(self, b'xPos')
            self.animation.setDuration(self.animation_duration)
            self.animation.setStartValue(self.xPos)
            self.animation.setEndValue(15)
            self.animation.setEasingCurve(self.easing_curve)
            self.animation.start()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        circle_position = QPoint(self.xPos, self.height() // 2)

        if self.checkState() == False:
            painter.setPen(QColor(self.outline_color))
            painter.setBrush(QColor(self.unchecked_color))
            center_coord = circle_position
        else:
            painter.setPen(QColor(self.outline_color))
            painter.setBrush(QColor(self.checked_color))
            center_coord = circle_position

        #draw border and circle inside of it regardless of state
        painter.drawRoundedRect(self.rect(), 17.5, 30.0)

        painter.setPen(QColor("white"))
        painter.setBrush(QColor("white"))
        painter.drawEllipse(center_coord, 10, 10)

class SidebarWidget(QFrame):
    #set custom signals so that mainwindow class can serve as the interface between sidebar and content area, separating them
    tracker_btn_clicked = pyqtSignal()
    settings_btn_clicked = pyqtSignal()

    def __init__(self, parent = None) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.setObjectName("SidebarWidget")

        self.tracker_btn = QPushButton("Price Tracker", self)
        self.settings_btn = QPushButton("Settings", self)

        

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
        cell1 = vbox_cell_widget("#######################", self)
        cell2 = vbox_cell_widget("apasa", self)

        togglebutton = ToggleButton()

        grid_layout.addWidget(cell1, 0, 0)
        grid_layout.addWidget(cell2, 0, 1)
        grid_layout.addWidget(togglebutton, 1, 0)

#stacked widget to display only one widget
class ContentArea(QStackedWidget):
    def __init__(self, parent = None, *args : QWidget) -> None:
        super().__init__()
        for widget in args:
            self.addWidget(widget)

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
        self.sidebar.tracker_btn_clicked.connect(
            lambda: self.content_area.widget_select(self.price_tracker_dash))
        
        self.sidebar.settings_btn_clicked.connect(
            lambda: self. content_area.widget_select(self.settings_dash))

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