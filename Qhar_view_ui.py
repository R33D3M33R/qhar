# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qhar_view.ui'
#
# Created: Tue Dec  2 12:51:49 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Qhar_ViewerEditor(object):
    def setupUi(self, Qhar_ViewerEditor):
        Qhar_ViewerEditor.setObjectName(_fromUtf8("Qhar_ViewerEditor"))
        Qhar_ViewerEditor.resize(864, 465)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Qhar_ViewerEditor)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.Qhar_ViewEdit = QtGui.QTabWidget(Qhar_ViewerEditor)
        self.Qhar_ViewEdit.setObjectName(_fromUtf8("Qhar_ViewEdit"))
        self.Qhar_view = QtGui.QWidget()
        self.Qhar_view.setObjectName(_fromUtf8("Qhar_view"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.Qhar_view)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableViewWidget = QtGui.QTableWidget(self.Qhar_view)
        self.tableViewWidget.setAlternatingRowColors(True)
        self.tableViewWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewWidget.setCornerButtonEnabled(False)
        self.tableViewWidget.setColumnCount(8)
        self.tableViewWidget.setObjectName(_fromUtf8("tableViewWidget"))
        self.tableViewWidget.setRowCount(0)
        self.tableViewWidget.horizontalHeader().setMinimumSectionSize(44)
        self.tableViewWidget.verticalHeader().setCascadingSectionResizes(True)
        self.verticalLayout.addWidget(self.tableViewWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_Filter = QtGui.QLabel(self.Qhar_view)
        self.label_Filter.setObjectName(_fromUtf8("label_Filter"))
        self.horizontalLayout.addWidget(self.label_Filter)
        self.comboBox_Filter = QtGui.QComboBox(self.Qhar_view)
        self.comboBox_Filter.setObjectName(_fromUtf8("comboBox_Filter"))
        self.horizontalLayout.addWidget(self.comboBox_Filter)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Add = QtGui.QPushButton(self.Qhar_view)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("list-add"))
        self.pushButton_Add.setIcon(icon)
        self.pushButton_Add.setObjectName(_fromUtf8("pushButton_Add"))
        self.horizontalLayout.addWidget(self.pushButton_Add)
        self.pushButton_Edit = QtGui.QPushButton(self.Qhar_view)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-edit"))
        self.pushButton_Edit.setIcon(icon)
        self.pushButton_Edit.setObjectName(_fromUtf8("pushButton_Edit"))
        self.horizontalLayout.addWidget(self.pushButton_Edit)
        self.pushButton_Close = QtGui.QPushButton(self.Qhar_view)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.pushButton_Close.setIcon(icon)
        self.pushButton_Close.setObjectName(_fromUtf8("pushButton_Close"))
        self.horizontalLayout.addWidget(self.pushButton_Close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.Qhar_ViewEdit.addTab(self.Qhar_view, _fromUtf8(""))
        self.Qhar_edit = QtGui.QWidget()
        self.Qhar_edit.setObjectName(_fromUtf8("Qhar_edit"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.Qhar_edit)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_Name = QtGui.QLabel(self.Qhar_edit)
        self.label_Name.setObjectName(_fromUtf8("label_Name"))
        self.gridLayout.addWidget(self.label_Name, 0, 0, 1, 1)
        self.lineEdit_Name = QtGui.QLineEdit(self.Qhar_edit)
        self.lineEdit_Name.setObjectName(_fromUtf8("lineEdit_Name"))
        self.gridLayout.addWidget(self.lineEdit_Name, 0, 1, 1, 1)
        self.label_Book = QtGui.QLabel(self.Qhar_edit)
        self.label_Book.setObjectName(_fromUtf8("label_Book"))
        self.gridLayout.addWidget(self.label_Book, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_Book = QtGui.QLineEdit(self.Qhar_edit)
        self.lineEdit_Book.setObjectName(_fromUtf8("lineEdit_Book"))
        self.horizontalLayout_2.addWidget(self.lineEdit_Book)
        self.label_Page = QtGui.QLabel(self.Qhar_edit)
        self.label_Page.setObjectName(_fromUtf8("label_Page"))
        self.horizontalLayout_2.addWidget(self.label_Page)
        self.spinBox_Page = QtGui.QSpinBox(self.Qhar_edit)
        self.spinBox_Page.setObjectName(_fromUtf8("spinBox_Page"))
        self.horizontalLayout_2.addWidget(self.spinBox_Page)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.label_TimeToCook = QtGui.QLabel(self.Qhar_edit)
        self.label_TimeToCook.setObjectName(_fromUtf8("label_TimeToCook"))
        self.gridLayout.addWidget(self.label_TimeToCook, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.spinBox_TimeToCook = QtGui.QSpinBox(self.Qhar_edit)
        self.spinBox_TimeToCook.setObjectName(_fromUtf8("spinBox_TimeToCook"))
        self.horizontalLayout_5.addWidget(self.spinBox_TimeToCook)
        self.checkBox_ExactTimeToCook = QtGui.QCheckBox(self.Qhar_edit)
        self.checkBox_ExactTimeToCook.setObjectName(_fromUtf8("checkBox_ExactTimeToCook"))
        self.horizontalLayout_5.addWidget(self.checkBox_ExactTimeToCook)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)
        self.label_LastCooked = QtGui.QLabel(self.Qhar_edit)
        self.label_LastCooked.setObjectName(_fromUtf8("label_LastCooked"))
        self.gridLayout.addWidget(self.label_LastCooked, 3, 0, 1, 1)
        self.dateEdit_LastCooked = QtGui.QDateEdit(self.Qhar_edit)
        self.dateEdit_LastCooked.setObjectName(_fromUtf8("dateEdit_LastCooked"))
        self.gridLayout.addWidget(self.dateEdit_LastCooked, 3, 1, 1, 1)
        self.label_RecipeType = QtGui.QLabel(self.Qhar_edit)
        self.label_RecipeType.setObjectName(_fromUtf8("label_RecipeType"))
        self.gridLayout.addWidget(self.label_RecipeType, 4, 0, 1, 1)
        self.comboBox_RecipeType = QtGui.QComboBox(self.Qhar_edit)
        self.comboBox_RecipeType.setObjectName(_fromUtf8("comboBox_RecipeType"))
        self.gridLayout.addWidget(self.comboBox_RecipeType, 4, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 244, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.pushButton_Save = QtGui.QPushButton(self.Qhar_edit)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save"))
        self.pushButton_Save.setIcon(icon)
        self.pushButton_Save.setObjectName(_fromUtf8("pushButton_Save"))
        self.horizontalLayout_6.addWidget(self.pushButton_Save)
        self.pushButton_Cancel = QtGui.QPushButton(self.Qhar_edit)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.pushButton_Cancel.setIcon(icon)
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.horizontalLayout_6.addWidget(self.pushButton_Cancel)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.Qhar_ViewEdit.addTab(self.Qhar_edit, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.Qhar_ViewEdit)

        self.retranslateUi(Qhar_ViewerEditor)
        self.Qhar_ViewEdit.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Qhar_ViewerEditor)

    def retranslateUi(self, Qhar_ViewerEditor):
        Qhar_ViewerEditor.setWindowTitle(_translate("Qhar_ViewerEditor", "Dialog", None))
        self.label_Filter.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.pushButton_Add.setText(_translate("Qhar_ViewerEditor", "PushButton", None))
        self.pushButton_Edit.setText(_translate("Qhar_ViewerEditor", "PushButton", None))
        self.pushButton_Close.setText(_translate("Qhar_ViewerEditor", "PushButton", None))
        self.label_Name.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.label_Book.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.label_Page.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.label_TimeToCook.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.checkBox_ExactTimeToCook.setText(_translate("Qhar_ViewerEditor", "CheckBox", None))
        self.label_LastCooked.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.label_RecipeType.setText(_translate("Qhar_ViewerEditor", "TextLabel", None))
        self.pushButton_Save.setText(_translate("Qhar_ViewerEditor", "PushButton", None))
        self.pushButton_Cancel.setText(_translate("Qhar_ViewerEditor", "PushButton", None))
        self.Qhar_ViewEdit.setTabText(self.Qhar_ViewEdit.indexOf(self.Qhar_edit), _translate("Qhar_ViewerEditor", "Stran", None))

