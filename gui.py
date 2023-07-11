import json
from PyQt6 import QtWidgets
from PyQt6 import QtGui

from gui_classes import CategoryFrame
from gui_classes import MenuAction

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
        service_menu = self.main_menu.addMenu('Сервис')

        add_category_action = MenuAction('Создать',
                                         'Ctrl+A',
                                         self.create_category,
                                         self.window)
        categoty_menu.addAction(add_category_action)

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

        exit_action = MenuAction('Выйти',
                                 'Ctrl+Q',
                                 self.exit,
                                 self.window)
        service_menu.addAction(exit_action)

        self.status_bar.showMessage('Программа загружена')
        self.window.show()

    def create_category(self, category):
        text_field = QtWidgets.QInputDialog()
        text_field.setLabelText('Название раздела:')
        text_field.show()
        text_field.exec()
        if not self.active_workspace:
            self.status_bar.showMessage('Нет активной рабочей среды')
        else:
            with open(f'workspaces/{self.active_workspace}.json', 'w') as workspace_file:
                workspace_dict = json.loads(workspace_file)
                workspace_dict['categories'].append(category)

    def create_workspace(self, workspace):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Название рабочей среды:')
        name_dialog.show()
        name_dialog.exec()
        self.active_workspace = name_dialog.textValue()
        self.status_bar.showMessage('Рабочая среда создана, но не сохранена')

    def load_workspace(self, workspace):
        with open(f'workspaces/{workspace}.json') as workspace_file:
            pass


if __name__ == '__main__':
    app = MainWindow()
    app.exec()
