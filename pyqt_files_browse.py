import sys
import os
from shutil import copyfile
import re
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
                            QGridLayout, QPushButton, QListView, QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication, Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PornHub Downloader'  # kek
        self.left = 256
        self.top = 256
        self.width = 1024
        self.height = 512
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #self.rootPath = 'D:/Hello Kotlin'  # TODO  change rootpath to dialog window
        self.dirDialog = QFileDialog()
        self.rootPath = self.dirDialog.getExistingDirectory()+"/"

        print("root path : ", self.rootPath)
        self.CWD = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/"
        print("CWD : ", self.CWD)

        # tree
        self.model = QFileSystemModel()
        self.model.setRootPath(self.rootPath)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.rootPath))
        self.tree.setSelectionMode(QTreeView.ExtendedSelection)
        self.tree.setColumnWidth(0, 361)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(3, True)
        
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(10)
        self.tree.setSortingEnabled(True)
        
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(320, 480)
        self.tree.move(10, 10)
        # ---------------------------------------
        # list
        self.model1 = QFileSystemModel()
        self.model1.setRootPath(self.rootPath)
        
        self.list = QListView()
        self.listModel = QStandardItemModel(self.list)
        
        self.list.setSelectionMode(QListView.ExtendedSelection)
        self.listModel = QStandardItemModel(self.list)
        self.list.setModel(self.listModel)

        # ----------------------------------------------
        # window layout setup
        # left box
        self.leftBox = QVBoxLayout()
        self.leftBox.addWidget(self.tree)
        self.addBtn = QPushButton("Add")
        self.leftBox.addWidget(self.addBtn)

        self.addBtn.clicked.connect(self.add_items)

       
        # right box
        self.rightBox = QVBoxLayout()

        self.rightBox.addWidget(self.list)
    
        self.removeBtn = QPushButton("Remove")
        self.rightBox.addWidget(self.removeBtn)
        
        # text box
        self.labelText = QLabel("Name for config:")
        
        self.textHolder = QLineEdit()

        self.textBox = QHBoxLayout()
        self.textBox.addWidget(self.labelText)
        self.textBox.addWidget(self.textHolder)


        # control btns
        self.saveBtn = QPushButton("Save Config")
        self.saveBtn.clicked.connect(self.confirmSelection)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(lambda:self.close())

        self.controlBox = QHBoxLayout()
        self.controlBox.addWidget(self.saveBtn)
        self.controlBox.addWidget(self.cancelBtn)


        # adding boxes to self.grid
        self.grid = QGridLayout()
        self.grid.addLayout(self.leftBox, 0, 0)
        self.grid.addLayout(self.rightBox, 0, 1)
        self.grid.addLayout(self.controlBox, 2, 1)
        self.grid.addLayout(self.textBox, 2, 0)

        self.removeBtn.clicked.connect(self.removeItems)

        self.setLayout(self.grid)
        # ------------------------------------------
        
        self.show()

    def add_items(self):
        indexes = self.tree.selectedIndexes()
        if indexes:
            self.fileDlgPaths = []  # prevent double indexes
            for i in indexes:
                path = self.model.filePath(i)
                if path not in self.fileDlgPaths:
                    self.fileDlgPaths.append(path)
            print(self.fileDlgPaths)
            for file in self.fileDlgPaths:
                self.add_file(file)
            self.list.setModel(self.listModel)
                
    

    def add_file(self, file):
        if os.path.isdir(file):
            return self.add_dir(file)
        list_of_items = self.listModel.findItems(file)
        for item in list_of_items:
            print(item.text())
        if len(list_of_items) == 0:
            item = QStandardItem(file)
            self.listModel.appendRow(item)
    
    def add_dir(self, dir):
        files = os.listdir(dir)
        for file in files:
            if os.path.isdir(file):
                self.add_dir(os.path.join(dir, file).replace("\\", "/"))
            else:
                self.add_file(os.path.join(dir, file).replace("\\", "/"))

    
    def removeItems(self):
        indexes = self.list.selectedIndexes()
        print("len", len(indexes))
        for index in range (len(indexes) - 1, -1, -1):
            print(indexes[index].row())
            self.listModel.takeRow(indexes[index].row())
    
    def confirmSelection(self):
        if self.listModel.rowCount() != 0:
            configName = self.textHolder.text()
            configName = re.sub("[^A-Za-z0-9_-]", "", configName)
            if len(configName) != 0:
                print(configName)
                os.makedirs(self.CWD + configName + "/")
                with open(f"{self.CWD}{configName}/{configName}_settings.cfg", "w") as file:
                    file.write("rootpath:" + self.rootPath)

                for i in range (self.listModel.rowCount()):
                    oldPath = self.listModel.item(i).text()
                    newPath = oldPath.replace(self.rootPath, self.CWD + configName + "/")
                    print("old path : ", oldPath)
                    print("new path : ", newPath)
                    print("lol : " + os.path.dirname(newPath))
                    try:
                        copyfile(oldPath, newPath)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(newPath))
                        copyfile(oldPath, newPath)

    def cancel(self):
        pass
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())