from PyQt6 import QtGui
from PyQt6 import QtCore
from PyQt6.QtCore import Qt


class MenuAction(QtGui.QAction):
    def __init__(self, name, shortcut, callback, parent):
        super().__init__(name, parent)
        self.setShortcut(shortcut)
        self.triggered.connect(callback)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.ItemDataRole.DisplayRole and Qt_Orientation == Qt.Orientation.Horizontal:
            header = ['Название', 'Цена', 'Количество']
            return header[p_int]
        else:
            return QtCore.QAbstractTableModel.headerData(self,
                                                         p_int,
                                                         Qt_Orientation,
                                                         role)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
