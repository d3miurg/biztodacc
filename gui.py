import json
from PyQt6 import QtWidgets

from gui_classes import MenuAction
from database import get_databases_names

class MainWindow(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])

        self.window = QtWidgets.QMainWindow()
        self.status_bar = self.window.statusBar()
        self.main_menu = self.window.menuBar()
        self.active_workspace = None
        self.active_category = None

        screen_size = self.screens()[0].availableSize()
        self.window.setGeometry(int(screen_size.width() / 4),
                                int(screen_size.height() / 4),
                                int(screen_size.width() / 2),
                                int(screen_size.height() / 2))
        self.window.setWindowTitle('Деловые Жабы: Учёт')

        workspace_menu = self.main_menu.addMenu('Рабочие среды')
        categoty_menu = self.main_menu.addMenu('Разделы')
        entry_menu = self.main_menu.addMenu('Вхождения')
        service_menu = self.main_menu.addMenu('Сервис')

        add_workspace_action = MenuAction('Создать',
                                          'Ctrl+N',
                                          self.create_workspace,
                                          self.window)
        workspace_menu.addAction(add_workspace_action)

        select_workspace_action = MenuAction('Загрузить',
                                             'Ctrl+L',
                                             self.load_workspace,
                                             self.window)
        workspace_menu.addAction(select_workspace_action)

        add_category_action = MenuAction('Создать',
                                         'Ctrl+C',
                                         self.create_category,
                                         self.window)
        categoty_menu.addAction(add_category_action)

        add_entry_action = MenuAction('Создать',
                                      'Ctrl+A',
                                      )

        exit_action = MenuAction('Выйти',
                                 'Ctrl+Q',
                                 self.exit,
                                 self.window)
        service_menu.addAction(exit_action)

        self.status_bar.showMessage('Программа загружена')
        self.window.show()

    def create_category(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Название раздела:')
        name_dialog.show()
        name_dialog.exec()
        if not self.active_workspace:
            self.status_bar.showMessage('Нет активной рабочей среды')
        else:
            self.active_category = name_dialog.textValue()

    def create_workspace(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Название рабочей среды:')
        name_dialog.show()
        name_dialog.exec()
        self.active_workspace = name_dialog.textValue()
        self.status_bar.showMessage('Рабочая среда создана, но не сохранена')

    def load_workspace(self):
        workspaces = get_databases_names()
        print(workspaces)


if __name__ == '__main__':
    app = MainWindow()
    app.exec()
