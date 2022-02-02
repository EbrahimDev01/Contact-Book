from PyQt5.QtWidgets import QDialog, QMessageBox
from GUIs.add_edit_show_information_contact_book_ui import Ui_Dialog
from contact_book_repository import ContactBookRepository
from group_name_repository import GroupNameRepository
import re

contact_book_repository = ContactBookRepository()
group_name_repository = GroupNameRepository()


class AddEditShowInformationContactBook(QDialog):
    def __init__(self, got_parent=None, got_item_id=None, got_editable=False):
        super(AddEditShowInformationContactBook, self).__init__(got_parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_events()
        self.item_id = got_item_id
        self.load_data_to_form(got_editable)
        self.exec_()

    def setup_events(self):
        self.ui.btn_cansle_contact_book.clicked.connect(self.close)
        self.ui.btn_save_contact_book.clicked.connect(self.event_clicked_btn_save_contact_book)

    def read_only_form(self):
        self.ui.btn_save_contact_book.hide()
        self.ui.line_edit_email.setReadOnly(True)
        self.ui.line_edit_first_name.setReadOnly(True)
        self.ui.line_edit_last_name.setReadOnly(True)
        self.ui.line_edit_phone_number.setReadOnly(True)
        self.ui.combo_box_group_name.setEnabled(False)

    def load_all_group_name_to_combo_box_group_name(self, item_id):
        group_names = group_name_repository.get_all_group_names()
        self.ui.combo_box_group_name.addItem('Select Group Name', None)
        for i, group_name in enumerate(group_names):
            self.ui.combo_box_group_name.addItem(group_name[1], group_name[0])
            if group_name[0] == item_id:
                self.ui.combo_box_group_name.setCurrentIndex(i + 1)

    def load_data_to_form(self, editable):
        group_name_id = None
        if self.item_id:
            if not editable:
                self.read_only_form()
            contact_book = contact_book_repository.get_contact_book_by_id(self.item_id)
            group_name_id = contact_book[-1]

            self.ui.line_edit_first_name.setText(contact_book[1])
            self.ui.line_edit_last_name.setText(contact_book[2])
            self.ui.line_edit_phone_number.setText(contact_book[3])
            self.ui.line_edit_email.setText(contact_book[4])
        self.load_all_group_name_to_combo_box_group_name(group_name_id)

    def get_data_form(self):
        return (self.ui.line_edit_first_name.text().strip(), self.ui.line_edit_last_name.text().strip(),
                self.ui.line_edit_phone_number.text().strip(), self.ui.line_edit_email.text().strip(),
                self.ui.combo_box_group_name.itemData(self.ui.combo_box_group_name.currentIndex()))

    def is_valid_data_form(self):
        data_form = self.get_data_form()
        text_msg = None

        if data_form[0] == '' and data_form[1] == '':
            text_msg = 'Enter First Name or Last Name'
        elif data_form[2] == '' and data_form[3] == '':
            text_msg = 'Enter Email or Phone Number'
        elif data_form[2] != '' and not re.fullmatch(r'09\d{9}', data_form[2]):
            text_msg = 'Format valid phone number is 09********* and len it should 11'
        elif data_form[3] != '' and not re.fullmatch(
                r"[A-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
                r"@(?:[A-z0-9](?:[A-z0-9-]*[A-z0-9])?\.)+[A-z0-9](?:[a-z0-9-]*[A-z0-9])?",
                data_form[3]):
            text_msg = 'Format valid Email is example@example.example'
        elif data_form[4] is None:
            text_msg = 'Select a Group Name'

        if text_msg is not None:
            QMessageBox(QMessageBox.Critical, 'Error', text_msg).exec_()

        return not bool(text_msg)

    def event_clicked_btn_save_contact_book(self):
        if self.is_valid_data_form():
            if self.item_id:
                self.edit_contact_book()
            else:
                self.insert_contact_book()
                self.clea_form()

    def edit_contact_book(self):
        data_form = self.get_data_form()
        contact_book_repository.edit_contact_book(self.item_id, *data_form)

    def insert_contact_book(self):
        data_form = self.get_data_form()
        contact_book_repository.insert_contact_book(*data_form)

    def clea_form(self):
        self.ui.line_edit_first_name.clear()
        self.ui.line_edit_last_name.clear()
        self.ui.line_edit_phone_number.clear()
        self.ui.line_edit_email.clear()
        self.ui.combo_box_group_name.setCurrentIndex(0)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = AddEditShowInformationContactBook(None)
    # ui.load_data_to_form(True)
    print(ui.get_data_form())
    sys.exit(app.exec_())
