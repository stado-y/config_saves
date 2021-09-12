import sys
from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QPushButton
    )
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication

class MainPage(QWidget):
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150
        self.widget()

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)

        # add label
        self.label1 = QLabel(self, text="Hello World!\nWelcome to PyQt5 Tutorial")
        # margin: left, top; width, height
        self.label1.setGeometry(QRect(50, 5, 100, 50))
        self.label1.setWordWrap(True) # allow word-wrap

        # add button
        self.btn1 = QPushButton(self, text="Submit")
        self.btn1.setToolTip("Change value of label")
        self.btn1.move(5, 95)
        self.btn1.clicked.connect(self.change_label)

        self.btn2 = QPushButton(self, text="Close")
        self.btn2.setToolTip("Exit window")
        self.btn2.move(95, 95)
        self.btn2.clicked.connect(self.exit_window)

        self.show()

    @pyqtSlot()
    def change_label(self):
        self.label1.setText("Submit button is pressed ")

    @pyqtSlot()
    def exit_window(self):
        QCoreApplication.instance().quit()

def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()