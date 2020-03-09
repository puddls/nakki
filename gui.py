from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QGridLayout, QLabel, QPushButton, QLCDNumber, QListWidget, QListWidgetItem, QLineEdit, QComboBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class MainWindow(QFrame):

    def __init__(self):
        super().__init__()


        layout = QGridLayout()
        self.action_drop = QComboBox()
        self.action_drop.addItem("Close")
        self.action_drop.addItem("Open")
        action_create = QPushButton("+")

        self.object_drop = QComboBox()
        self.object_drop.addItem("Discord")
        self.object_drop.addItem("Spotify")
        object_create = QPushButton("+")

        self.cond_drop = QComboBox()
        self.cond_drop.addItem("9 AM")
        self.cond_drop.addItem("2 PM")
        cond_create = QPushButton("+")

        self.theme_button = QPushButton("Dark Mode")

        action_create.clicked.connect(self.create_action_block)
        object_create.clicked.connect(self.create_object_block)
        cond_create.clicked.connect(self.create_cond_block)

        self.theme_button.clicked.connect(self.theme_change)

        layout.addWidget(self.action_drop, 1, 1, 1, 3)
        layout.addWidget(action_create, 1, 4, 1, 1)

        layout.addWidget(self.object_drop, 1, 5, 1, 3)
        layout.addWidget(object_create, 1, 8, 1, 1)

        layout.addWidget(self.cond_drop, 1, 9, 1, 3)
        layout.addWidget(cond_create, 1, 12, 1, 1)

        layout.addWidget(self.theme_button,2,1,1,1)

        self.setLayout(layout)

    def create_action_block(self):
        print("no work")

    def create_object_block(self):
        print("no work")

    def create_cond_block(self):
        print("no work")

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
