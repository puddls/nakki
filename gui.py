from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QGridLayout, QLabel, QPushButton, QLCDNumber, QListWidget, QListWidgetItem, QLineEdit, QComboBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class MainWindow(QFrame):

    def __init__(self):
        super().__init__()


        layout = QGridLayout()
        action_drop = QComboBox()
        action_drop.addItem("Close")
        action_drop.addItem("Open")
        action_create = QPushButton("+")

        object_drop = QComboBox()
        object_drop.addItem("Discord")
        object_drop.addItem("Spotify")
        object_create = QPushButton("+")

        cond_drop = QComboBox()
        cond_drop.addItem("9 AM")
        cond_drop.addItem("2 PM")
        cond_create = QPushButton("+")

        layout.addWidget(action_drop, 1, 1, 1, 3)
        layout.addWidget(action_create, 1, 4, 1, 1)
        
        layout.addWidget(object_drop, 1, 5, 1, 3)
        layout.addWidget(object_create, 1, 8, 1, 1)

        layout.addWidget(cond_drop, 1, 9, 1, 3)
        layout.addWidget(cond_create, 1, 12, 1, 1)

        self.setLayout(layout)


app = QApplication([])
app.setStyle("Fusion")
app.setApplicationName("Nakki")

window = MainWindow()
window.resize(600, 750)
window.show()

# set dark theme
# from https://stackoverflow.com/a/56851493/12164878
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

app.exec_()
