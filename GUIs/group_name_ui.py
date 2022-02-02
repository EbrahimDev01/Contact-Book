# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Designs\group_name_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 520)
        Dialog.setMinimumSize(QtCore.QSize(800, 520))
        Dialog.setMaximumSize(QtCore.QSize(800, 16777215))
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_edit_search = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.gridLayout.addWidget(self.line_edit_search, 0, 1, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 781, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_widget_group_names = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.table_widget_group_names.setObjectName("table_widget_group_names")
        self.table_widget_group_names.setColumnCount(0)
        self.table_widget_group_names.setRowCount(0)
        self.verticalLayout.addWidget(self.table_widget_group_names)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_add_group_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_add_group_name.setObjectName("btn_add_group_name")
        self.horizontalLayout_2.addWidget(self.btn_add_group_name)
        self.btn_edit_group_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_edit_group_name.setObjectName("btn_edit_group_name")
        self.horizontalLayout_2.addWidget(self.btn_edit_group_name)
        self.btn_show_info_group_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_show_info_group_name.setObjectName("btn_show_info_group_name")
        self.horizontalLayout_2.addWidget(self.btn_show_info_group_name)
        self.btn_delete_group_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_delete_group_name.setObjectName("btn_delete_group_name")
        self.horizontalLayout_2.addWidget(self.btn_delete_group_name)
        self.btn_refresh_group_name = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_refresh_group_name.setObjectName("btn_refresh_group_name")
        self.horizontalLayout_2.addWidget(self.btn_refresh_group_name)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "search"))
        self.btn_add_group_name.setText(_translate("Dialog", "Add"))
        self.btn_edit_group_name.setText(_translate("Dialog", "Edit"))
        self.btn_show_info_group_name.setText(_translate("Dialog", "Show Info"))
        self.btn_delete_group_name.setText(_translate("Dialog", "Delete"))
        self.btn_refresh_group_name.setText(_translate("Dialog", "Refresh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())