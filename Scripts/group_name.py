import sys
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from GUIs.group_name_ui import Ui_Dialog
from group_name_repository import GroupNameRepository
from add_edit_show_information_group_name import AddEditShowInformationGroupName

group_name_repository = GroupNameRepository()


class GroupName(QDialog):
    def __init__(self):
        super(GroupName, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_events()
        self.refresh_table_widget_group_names()
        self.ui.table_widget_group_names.hideColumn(0)
        self.ui.table_widget_group_names.setHorizontalHeaderLabels(['', 'Group Name'])
        self.child_window = None
        self.exec_()

    def setup_events(self):
        # setup events button
        self.ui.btn_refresh_group_name.clicked.connect(self.refresh_table_widget_group_names)
        self.ui.btn_delete_group_name.clicked.connect(self.delete_group_name)
        self.ui.btn_add_group_name.clicked.connect(self.create_child_window_add_group_name)
        self.ui.btn_edit_group_name.clicked.connect(self.create_child_window_edit_group_name)
        self.ui.btn_show_info_group_name.clicked.connect(self.create_child_window_show_info_group_name)

        self.ui.line_edit_search.textChanged.connect(self.search_group_name)

    def refresh_table_widget_group_names(self):
        group_names_list = group_name_repository.get_all_group_names()
        self.load_data_to_table_widget_group_names(group_names_list)
        self.ui.line_edit_search.clear()

    def load_data_to_table_widget_group_names(self, group_names_list):
        self.ui.table_widget_group_names.clearContents()
        self.ui.table_widget_group_names.setRowCount(len(group_names_list))

        if group_names_list:
            self.ui.table_widget_group_names.setColumnCount(len(group_names_list[0]))
            for row, group_name_data in enumerate(group_names_list):
                for column, group_name in enumerate(group_name_data):
                    item = QTableWidgetItem(str(group_name))
                    item.setFlags(Qt.ItemIsEnabled)
                    self.ui.table_widget_group_names.setItem(row, column, item)

    def get_id_row_item_in_table(self):
        current_row = self.ui.table_widget_group_names.currentRow()
        if current_row >= 0:
            item_id = self.ui.table_widget_group_names.item(current_row, 0).text()
            return int(item_id)
        QMessageBox(QMessageBox.Critical, 'Error', 'Select Row').exec_()
        return False

    def delete_group_name(self):
        group_name_id = self.get_id_row_item_in_table()
        if group_name_id:
            result = group_name_repository.delete_group_name_by_id(group_name_id)
            if result:
                QMessageBox(QMessageBox.Critical, 'Error', result).exec_()
            self.refresh_table_widget_group_names()

    def search_group_name(self):
        group_name_title = self.ui.line_edit_search.text().strip()
        if len(group_name_title) > 0:
            group_names = group_name_repository.search_group_name(group_name_title)
            self.load_data_to_table_widget_group_names(group_names)
        else:
            self.refresh_table_widget_group_names()

    def create_child_window_add_group_name(self):
        self.child_window = AddEditShowInformationGroupName(self, None, True)
        self.refresh_table_widget_group_names()

    def create_child_window_edit_group_name(self):
        item_id = self.get_id_row_item_in_table()
        if item_id:
            self.child_window = AddEditShowInformationGroupName(self, item_id, True)
            self.refresh_table_widget_group_names()

    def create_child_window_show_info_group_name(self):
        item_id = self.get_id_row_item_in_table()
        if item_id:
            self.child_window = AddEditShowInformationGroupName(self, item_id, False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GroupName()
    sys.exit(app.exec_())
