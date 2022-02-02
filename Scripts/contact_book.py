from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from GUIs import contact_book_ui
from contact_book_repository import ContactBookRepository, initialize_database
from group_name_repository import GroupNameRepository
from add_edit_show_information_contact_book import AddEditShowInformationContactBook
from group_name import GroupName

initialize_database()
contact_book_repository = ContactBookRepository()
group_name_repository = GroupNameRepository()


class ContactBook(QMainWindow):
    def __init__(self):
        super(ContactBook, self).__init__()
        self.ui = contact_book_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_events()
        self.refresh_contact_books_form()
        self.ui.table_widget_contact_list.setHorizontalHeaderLabels(
            ['', 'First Name', 'Last Name', 'Phone Number', 'Email', 'Group Name'])
        self.ui.table_widget_contact_list.hideColumn(0)
        self.child_window = None
        self.msg = None
        self.show()

    def setup_events(self):
        # setup events button
        self.ui.btn_refresh_contact_book.clicked.connect(self.refresh_contact_books_form)
        self.ui.btn_delete_contact_book.clicked.connect(self.delete_contact_book)
        self.ui.btn_add_contact_book.clicked.connect(self.show_add_contact_book_window)
        self.ui.btn_edit_contact_book.clicked.connect(self.show_edit_contact_book_window)
        self.ui.btn_show_info_contact_book.clicked.connect(self.show_information_contact_book_window)
        self.ui.btn_group_name_control.clicked.connect(self.show_group_name)
        # setup events line edit
        self.ui.line_edit_search.textEdited.connect(self.search_contact_book_load_to_table)

        self.ui.combo_box_group_name.currentIndexChanged.connect(self.search_contact_book_load_to_table)

    def search_contact_book(self):
        contact_book_title = self.ui.line_edit_search.text().strip()
        index = self.ui.combo_box_group_name.currentIndex()
        group_name_id = self.ui.combo_box_group_name.itemData(index)
        return contact_book_repository.search_contact_book(contact_book_title, group_name_id)

    def search_contact_book_load_to_table(self):
        group_names = group_name_repository.get_all_group_names()
        self.load_contact_book_to_tabel(self.search_contact_book(), group_names)

    def refresh_contact_books_form(self):
        self.ui.line_edit_search.clear()
        # contact_books = contact_book_repository.get_all_contact_books()
        group_names = group_name_repository.get_all_group_names()
        self.load_contact_book_combo_box_group_name(group_names)
        # self.load_contact_book_to_tabel(contact_books, group_names)

    def load_contact_book_to_tabel(self, contact_books_list, group_names_list):
        self.ui.table_widget_contact_list.clearContents()
        self.ui.table_widget_contact_list.setRowCount(len(contact_books_list))
        self.ui.table_widget_contact_list.setColumnCount(6)

        for i, items in enumerate(contact_books_list):
            items = list(items)

            # get group name title by group id in items
            # itme 5 is group name id
            for group_name in group_names_list:
                if group_name[0] == items[5]:
                    items[5] = group_name[1]
                    break

            for x, item in enumerate(items):
                widget_item = QTableWidgetItem(str(item))
                widget_item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_widget_contact_list.setItem(i, x, widget_item)

    def load_contact_book_combo_box_group_name(self, group_names_list):
        self.ui.combo_box_group_name.clear()
        self.ui.combo_box_group_name.addItem('All Group', None)
        for group_name in group_names_list:
            self.ui.combo_box_group_name.addItem(group_name[1], group_name[0])

    def get_id_contact_book_by_table(self):
        if (current_row := self.ui.table_widget_contact_list.currentRow()) >= 0:
            item_id = self.ui.table_widget_contact_list.item(current_row, 0).text()
            return int(item_id)
        self.msg = QMessageBox(self)
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText('select row')
        self.msg.show()
        return False

    def delete_contact_book(self):
        item_id = self.get_id_contact_book_by_table()
        if item_id:
            contact_book_repository.delete_contact_by_id(item_id)
            self.search_contact_book_load_to_table()

    def show_add_contact_book_window(self):
        self.child_window = AddEditShowInformationContactBook(self)
        self.refresh_contact_books_form()

    def show_edit_contact_book_window(self):
        item_id = self.get_id_contact_book_by_table()
        if item_id:
            self.child_window = AddEditShowInformationContactBook(self, item_id, True)
            self.refresh_contact_books_form()

    def show_information_contact_book_window(self):
        item_id = self.get_id_contact_book_by_table()
        if item_id:
            self.child_window = AddEditShowInformationContactBook(self, item_id, False)

    def show_group_name(self):
        self.child_window = GroupName()
        group_names_list = group_name_repository.get_all_group_names()
        self.load_contact_book_combo_box_group_name(group_names_list)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = ContactBook()
    sys.exit(app.exec_())
