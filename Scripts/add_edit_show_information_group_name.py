from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QSize, QRect
from GUIs.add_edit_show_information_group_name_ui import Ui_Dialog
from group_name_repository import GroupNameRepository
from contact_book_repository import ContactBookRepository

group_name_repository = GroupNameRepository()
contact_book_repository = ContactBookRepository()


class AddEditShowInformationGroupName(QDialog):
    def __init__(self, parent=None, group_name_id=None, editable=True):
        super(AddEditShowInformationGroupName, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_events()
        self.group_name_id = group_name_id
        self.setup(editable)
        self.exec_()

    def setup_events(self):
        self.ui.btn_cansle_group_name.clicked.connect(self.close)
        self.ui.btn_save_group_name.clicked.connect(self.event_btn_save_group_name)

    def disable_form(self):
        self.ui.line_edit_group_name.setEnabled(False)
        self.ui.btn_save_group_name.hide()

    def setup(self, editable):
        if self.group_name_id:
            if not editable:
                self.disable_form()
            group_name_title = group_name_repository.get_group_name_by_id(self.group_name_id)[1]
            self.ui.line_edit_group_name.setText(group_name_title)
            contact_books = contact_book_repository.get_contact_book_by_group_name_id(self.group_name_id)
            self.load_data_contact_book_to_table(contact_books)
            self.ui.table_widget_contact_group_name.setHorizontalHeaderLabels(
                ['First Name', 'Last Name', 'Phone Number', 'Email'])
        else:
            self.ui.table_widget_contact_group_name.hide()
            self.ui.label_contact_this_group_name.hide()
            self.setMaximumSize(QSize(540, 70))

    def load_data_contact_book_to_table(self, contact_books_list):
        if not contact_books_list:
            return
        self.ui.table_widget_contact_group_name.clearContents()
        self.ui.table_widget_contact_group_name.setRowCount(len(contact_books_list))
        self.ui.table_widget_contact_group_name.setColumnCount(len(contact_books_list[0]) - 2)
        for row, items in enumerate(contact_books_list):
            for column in range(1, len(items)):
                item = QTableWidgetItem(str(items[column]))
                item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_widget_contact_group_name.setItem(row, column - 1, item)

    def event_btn_save_group_name(self):
        if self.group_name_id:
            self.edit_group_name()
        else:
            self.add_group_name()

    def get_group_name_title(self):
        group_name_title = self.ui.line_edit_group_name.text().strip()

        if len(group_name_title) <= 0:
            QMessageBox(QMessageBox.Critical, 'Error', 'Pleas Enter Group Name Title').exec_()
            return False
        if group_name_repository.is_exists_by_title_and_id(group_name_title):
            QMessageBox(QMessageBox.Critical, 'Error', 'this title is exist for group name').exec_()
            return False
        return group_name_title

    def add_group_name(self):
        group_name_title = self.get_group_name_title()
        if group_name_title:
            group_name_repository.add_group_name(group_name_title)
            self.ui.line_edit_group_name.clear()

    def edit_group_name(self):
        group_name_title = self.get_group_name_title()
        if group_name_title:
            group_name_repository.edit_group_name(group_name_title, self.group_name_id)
            self.close()
