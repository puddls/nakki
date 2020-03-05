from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QGridLayout, QLabel, QPushButton, QLCDNumber, QListWidget, QListWidgetItem, QLineEdit
from PyQt5.QtGui import QPalette, QColor


class MainWindow(QFrame):

    def __init__(self):
        super().__init__()


        layout = QGridLayout()


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
