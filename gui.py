from PyQt6 import QtWidgets

from gui_classes import MenuAction
from gui_classes import TableModel
from database import get_databases_names
from database import create_new_entry
from database import check_connection
from database import get_collections_names
from database import get_entries_names
from database import delete_database
from database import delete_collection
from database import delete_entry


class MainWindow(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])

        self.window = QtWidgets.QMainWindow()
        self.status_bar = self.window.statusBar()
        self.main_menu = self.window.menuBar()
        print(self.main_menu.size().height())
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
                                          'Ctrl+N+W',
                                          self.create_workspace,
                                          self.window)
        workspace_menu.addAction(add_workspace_action)

        select_workspace_action = MenuAction('Загрузить',
                                             'Ctrl+L+W',
                                             self.load_all_workspaces,
                                             self.window)
        workspace_menu.addAction(select_workspace_action)

        delete_workspace_action = MenuAction('Удалить',
                                             'Ctrl+D+W',
                                             self.delete_workspace,
                                             self.window)
        workspace_menu.addAction(delete_workspace_action)

        add_category_action = MenuAction('Создать',
                                         'Ctrl+N+C',
                                         self.create_category,
                                         self.window)
        categoty_menu.addAction(add_category_action)

        delete_category_action = MenuAction('Удалить',
                                            'Ctrl+D+C',
                                            self.delete_category,
                                            self.window)
        categoty_menu.addAction(delete_category_action)

        create_entry_action = MenuAction('Создать',
                                         'Ctrl+N+E',
                                         self.create_entry,
                                         self.window)
        entry_menu.addAction(create_entry_action)

        delete_entry_action = MenuAction('Удалить',
                                         'Ctrl+D+E',
                                         self.delete_entry,
                                         self.window)
        entry_menu.addAction(delete_entry_action)

        exit_action = MenuAction('Выйти',
                                 'Ctrl+Q',
                                 self.exit,
                                 self.window)
        service_menu.addAction(exit_action)

        names = check_connection()
        if names:
            self.status_bar.showMessage('Программа загружена')
        else:
            self.status_bar.showMessage('Не удалось подключиться к базе данных. Перезапустите приложение')
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
            self.status_bar.showMessage('Раздел создан, но не сохранена')

    def create_workspace(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Название рабочей среды:')
        name_dialog.show()
        name_dialog.exec()
        self.active_workspace = name_dialog.textValue()
        self.status_bar.showMessage('Рабочая среда создана, но не сохранена')

    def load_workspace(self, workspaces_list):
        self.active_workspace = workspaces_list.selectedItems()[0].text()
        workspaces_list.hide()
        categories = get_collections_names(self.active_workspace)
        categories_list = QtWidgets.QListWidget(self.window)
        [categories_list.addItem(n) for n in categories]
        categories_list.setGeometry(0,
                                    self.main_menu.size().height(),
                                    self.window.geometry().width(),
                                    self.window.geometry().height() - self.status_bar.size().height() * 2)
        categories_list.itemClicked.connect(lambda: self.load_category(categories_list))
        categories_list.show()
        self.status_bar.showMessage('Разделы загружены')

    def load_all_workspaces(self):
        workspaces = get_databases_names()
        workspaces_list = QtWidgets.QListWidget(self.window)
        [workspaces_list.addItem(n) for n in workspaces]
        workspaces_list.setGeometry(0,
                                    self.main_menu.size().height(),
                                    self.window.geometry().width(),
                                    self.window.geometry().height() - self.status_bar.size().height() * 2)
        workspaces_list.itemClicked.connect(lambda: self.load_workspace(workspaces_list))
        workspaces_list.show()
        print(workspaces)
        self.status_bar.showMessage('Рабочие среды загружены')

    def create_entry(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Название:')
        name_dialog.show()
        name_dialog.exec()

        price_dialog = QtWidgets.QInputDialog()
        price_dialog.setLabelText('Цена:')
        price_dialog.show()
        price_dialog.exec()

        count_dialog = QtWidgets.QInputDialog()
        count_dialog.setLabelText('Количество:')
        count_dialog.show()
        count_dialog.exec()

        if not self.active_category:
            self.status_bar.showMessage('Нет активной категории')
        else:
            create_new_entry(self.active_workspace,
                             self.active_category,
                             name_dialog.textValue(),
                             price_dialog.textValue(),
                             count_dialog.textValue())
            self.status_bar.showMessage('Вхождение создано и сохранено')

    def load_category(self, categories_list):
        self.active_category = categories_list.selectedItems()[0].text()
        categories_list.hide()
        entries = get_entries_names(self.active_workspace,
                                    self.active_category)
        entries_table = QtWidgets.QTableView(self.window)
        model = TableModel(entries)
        entries_table.setModel(model)
        entries_table.setGeometry(0,
                                  self.main_menu.size().height(),
                                  self.window.geometry().width(),
                                  self.window.geometry().height() - self.status_bar.size().height() * 2)
        entries_table.show()
        self.status_bar.showMessage('Категории загружены')

    def delete_workspace(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Рабочая среда:')
        name_dialog.show()
        name_dialog.exec()

        delete_database(name_dialog.textValue())

    def delete_category(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Раздел:')
        name_dialog.show()
        name_dialog.exec()

        delete_collection(self.active_workspace, name_dialog.textValue())

    def delete_entry(self):
        name_dialog = QtWidgets.QInputDialog()
        name_dialog.setLabelText('Раздел:')
        name_dialog.show()
        name_dialog.exec()

        delete_entry(self.active_workspace,
                     self.active_category,
                     name_dialog.textValue())


if __name__ == '__main__':
    app = MainWindow()
    app.exec()
