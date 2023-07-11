from PyQt6 import QtWidgets
from PyQt6 import QtGui


class MenuAction(QtGui.QAction):
    def __init__(self, name, shortcut, callback, parent):
        super().__init__(name, parent)
        self.setShortcut(shortcut)
        self.triggered.connect(callback)


class CategoryFrame(QtWidgets.QFrame):
    def __init__(self, category_name):
        super().__init__()
        self.category_name = category_name
