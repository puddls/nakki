from random import randint

from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QGridLayout, QLabel,
                             QPushButton, QListWidget, QListWidgetItem, QLineEdit, QComboBox,
                             QTabWidget, QScrollArea, QSizePolicy)
from PyQt5.QtGui import QBrush, QColor, QDrag, QPainter, QPalette, QPen, QPolygon, QRegion
from PyQt5.QtCore import QMimeData, QPoint, Qt, pyqtSignal

from systemctl.controller_factory import systemController


class MainWindow(QFrame):

    def __init__(self):
        super().__init__()

        settings = Settings()
        create_page = CreateTaskPage()

        self.tabs = QTabWidget()
        self.tabs.addTab(create_page, "Actions")
        self.tabs.addTab(settings, "Settings")
        # Need to implement task list class

        self.layout = QGridLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class CreateTaskPage(QFrame):

    def __init__(self):
        super().__init__()

        self.buttons = ConstructionButtons()
        self.buttons.action_create.clicked.connect(self.create_action_block)
        self.buttons.object_create.clicked.connect(self.create_object_block)
        self.buttons.cond_create.clicked.connect(self.create_cond_block)

        self.creation_box = CreationZone()

        name_box = QLineEdit()
        name_box.setPlaceholderText("Enter the name of your task here.")

        save = QPushButton("Save")
        save.clicked.connect(self.save_task)

        self.layout = QGridLayout()
        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.creation_box)
        self.layout.addWidget(name_box)
        self.layout.addWidget(save)
        self.setLayout(self.layout)

    def save_task(self):
        print("no work")

    def create_action_block(self):
        actionW = ActionWidget(self.buttons.action_drop.currentData())
        self.creation_box.add_construction_label(actionW)

    def create_object_block(self):
        objectW = ObjectWidget(self.buttons.object_drop.currentData())
        self.creation_box.add_construction_label(objectW)

    def create_cond_block(self):
        condW = CondWidget(self.buttons.cond_drop.currentData())
        self.creation_box.layout.addWidget(condW
        )

class ConstructionButtons(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()

        self.action_drop = QComboBox()
        self.action_drop.addItem("Close", "Close")
        self.action_drop.addItem("Open", "Open")
        self.action_create = QPushButton("+")
        self.action_create.setStyleSheet("padding: 3px;")

        self.object_drop = QComboBox()
        apps = systemController.get_applications()
        if apps:
            for application in apps:
                self.object_drop.addItem(application[0], application[0])
        else:
            self.object_drop.addItem("No apps found", "No apps found")
        self.object_create = QPushButton("+")
        self.object_create.setStyleSheet("padding: 3px;")

        self.cond_drop = QComboBox()
        self.cond_drop.addItem("9 AM", "9 AM")
        self.cond_drop.addItem("2 PM", "2 PM")
        self.cond_create = QPushButton("+")
        self.cond_create.setStyleSheet("padding: 3px;")

        self.layout.addWidget(self.cond_drop, 1, 1, 1, 3)
        self.layout.addWidget(self.cond_create, 1, 4, 1, 1)

        self.layout.addWidget(self.action_drop, 1, 5, 1, 3)
        self.layout.addWidget(self.action_create, 1, 8, 1, 1)

        self.layout.addWidget(self.object_drop, 1, 9, 1, 3)
        self.layout.addWidget(self.object_create, 1, 12, 1, 1)

        self.setLayout(self.layout)


class CreationZone(QScrollArea):
    GRID_WIDTH = 100
    GRID_HEIGHT = 100
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def add_construction_label(self, construction_label):
        x = randint(0, self.GRID_WIDTH)
        y = randint(0, self.GRID_HEIGHT)
        # TODO
        # ideas:
        # prefill every 100x100 slot with a blank widget (spacer maybe?)
        # then just replace the widget at that xy with the construction label
        # instead of adding it.
        # could run into issues because the labels have a larger span than just
        # 1 grid spot

        self.layout.addWidget(construction_label, x, y)

    def dragEnterEvent(self, event):
        # need to accept the event so qt gives us the DropEvent
        # https://doc.qt.io/qt-5/qdropevent.html#details
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimedata = event.mimeData()
        event.acceptProposedAction()
        print("dropped")
        # TODO
        # @ kate - work your magic!

class ConstructionLabel(QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        # this is a beyond dirty hack but I couldn't get it to size properly
        # horizontally with size policies alone
        self.setFixedWidth(100)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mouseMoveEvent(self, event):
        drag = QDrag(self)
        # make the drag look like our widget
        pixmap = self.grab()
        drag.setPixmap(pixmap)
        # empty for now
        mime_data = QMimeData()
        drag.setMimeData(mime_data)
        drag.exec()


class ActionWidget(ConstructionLabel):
    def __init__(self, name):
        super().__init__(name)
        point1 = QPoint(0, 0)
        point2 = QPoint(80, 0)
        point3 = QPoint(92, 10)
        point4 = QPoint(80, 20)
        point5 = QPoint(0, 20)
        point6 = QPoint(12, 10)
        self.poly = QPolygon((point1, point2, point3, point4, point5, point6))
        region = QRegion(self.poly)
        self.setMask(region)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(QBrush(QColor("#000")), 2))
        painter.drawPolygon(self.poly)

class ObjectWidget(ConstructionLabel):
    def __init__(self, name):
        super().__init__(name)
        point1 = QPoint(0, 0)
        point2 = QPoint(80, 0)
        point3 = QPoint(92, 10)
        point4 = QPoint(80, 20)
        point5 = QPoint(0, 20)
        point6 = QPoint(12, 10)
        self.poly = QPolygon((point1, point2, point3, point4, point5, point6))
        region = QRegion(self.poly)
        self.setMask(region)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(QBrush(QColor("#000")), 2))
        painter.drawPolygon(self.poly)

class CondWidget(ConstructionLabel):
    def __init__(self, name):
        super().__init__(name)
        point1 = QPoint(0, 0)
        point2 = QPoint(80, 0)
        point3 = QPoint(92, 10)
        point4 = QPoint(80, 20)
        point5 = QPoint(0, 20)
        self.poly = QPolygon((point1, point2, point3, point4, point5))
        region = QRegion(self.poly)
        self.setMask(region)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(QPen(QBrush(QColor("#000")), 1))
        painter.drawPolygon(self.poly)


class Settings(QFrame):
    def __init__(self):
        super().__init__()

        self.theme_button = QPushButton("Dark Mode")
        self.theme_button.clicked.connect(self.theme_change)

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.theme_button, 1, 1)

        self.setLayout(self.layout)

    def theme_change(self):
        if self.theme_button.text() == "Dark Mode":
            app.setPalette(dark_mode)
            self.theme_button.setText("Light Mode")
        else:
            app.setPalette(app.style().standardPalette())
            self.theme_button.setText("Dark Mode")

app = QApplication([])
app.setStyle("Fusion")
app.setApplicationName("Nakki")

window = MainWindow()
window.resize(600, 750)
window.show()

# dark theme
# from https://stackoverflow.com/a/56851493/12164878
dark_mode = QPalette()
dark_mode.setColor(QPalette.Window, QColor(53, 53, 53))
dark_mode.setColor(QPalette.WindowText, Qt.white)
dark_mode.setColor(QPalette.Base, QColor(25, 25, 25))
dark_mode.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_mode.setColor(QPalette.ToolTipBase, Qt.white)
dark_mode.setColor(QPalette.ToolTipText, Qt.white)
dark_mode.setColor(QPalette.Text, Qt.white)
dark_mode.setColor(QPalette.Button, QColor(53, 53, 53))
dark_mode.setColor(QPalette.ButtonText, Qt.white)
dark_mode.setColor(QPalette.BrightText, Qt.red)
dark_mode.setColor(QPalette.Link, QColor(42, 130, 218))
dark_mode.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_mode.setColor(QPalette.HighlightedText, Qt.black)

app.exec_()
