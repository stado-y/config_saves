import sys
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PornHub Downloader'
        self.left = 256
        self.top = 256
        self.width = 1024
        self.height = 512
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        

        # first tree
        self.model = QFileSystemModel()
        self.model.setRootPath('D:/Hello Kotlin')
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('D:/Hello Kotlin'))
        self.tree.setSelectionMode(QTreeView.MultiSelection)
        
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(10)
        self.tree.setSortingEnabled(True)
        
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(320, 480)
        self.tree.move(10, 10)
        # ---------------------------------------
        # second tree
        self.model1 = QFileSystemModel()
        self.model1.setRootPath('D:/Hello Kotlin')
        
        self.tree1 = QTreeView()
        self.tree1.setModel(self.model1)
        self.tree1.setRootIndex(self.model1.index('D:/Hello Kotlin'))
        self.tree.setSelectionMode(QTreeView.MultiSelection)
        
        
        self.tree1.setAnimated(False)
        self.tree1.setIndentation(10)
        self.tree1.setSortingEnabled(True)
        
        self.tree1.setWindowTitle("Dir View2")
        self.tree1.resize(320, 480)
        self.tree1.move(340, 10)
        print(self.model1.index('D:/Hello Kotlin'))
        # ----------------------------------------------
        # window layout setup
        # left box
        leftBox = QVBoxLayout()
        leftBox.addWidget(self.tree)
        addBtn = QPushButton("Add")
        leftBox.addWidget(addBtn)

        addBtn.clicked.connect(self.add_items)

       
        # right box
        rightBox = QVBoxLayout()
        rightBox.addWidget(self.tree1)
        rightBox.addWidget(QPushButton("Remove"))
        # adding boxes to grid
        grid = QGridLayout()
        grid.addLayout(leftBox,0,0)
        grid.addLayout(rightBox,0,1)

        self.setLayout(grid)
        # ------------------------------------------
        
        self.show()

    def add_items(self):
        print(self.tree.selectedIndexes())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())