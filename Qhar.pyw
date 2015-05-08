#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "Andrej Mernik"
__copyright__ = "(C) 2014 Andrej Mernik"
__version__ = "0.1"
__license__ = "GPLv3"

# This file is part of Qhar.
# Qhar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Qhar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Qhar.  If not, see <http://www.gnu.org/licenses/>.

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Qhar_main_ui import *
from Qhar_data import *
from Qhar_files import *
from Qhar_settings import *
from Qhar_view import *


class Qhar_MainWindow(RecipeContainer, QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Qhar_MainWindow, self).__init__()
        self.setupUi(self)
        self.load_settings()
        self.create_items()
        self.connect_actions_and_signals()
        self.set_recipe_filter(True)
        self.file_open(True)

    def create_items(self):
        """Create items which which were not created with Qt designer. This
        method is run only at startup"""
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDisplayFormat(self.date_string)
        self.dateEdit.setDate(self.current_date)
        self.label_filter.setText("Filter")
        self.comboBox_filter.addItem("All")
        self.comboBox_filter.addItems(list(self.recipe_types.values()))
        self.pushButton_select.setText("Select")
        self.pushButton_select.setHidden(True)
        tables = [self.tableWidget_view, self.tableWidget_week]
        horizontal_header_labels = [" ", "Main Dish ID", self.arguments["name"],
                                    self.arguments["book"], self.arguments["page"],
                                    self.arguments["time_to_cook"], self.arguments["side_dish_id"],
                                    self.arguments["side_dish_id"].replace("ID", "")]
        for table in tables:
            table.setHorizontalHeaderLabels(horizontal_header_labels)
            table.verticalHeader().setResizeMode(QHeaderView.Stretch)
            table.setColumnWidth(0, 5)
            table.setColumnHidden(1, True)
            table.setColumnHidden(6, True)

    def status_row_label(self, id, status):
        """Create a custom QLabel which doesn't get deleted when table
        contents are cleared"""
        if status == "TODAY":
            color = "yellow"
        elif status == "INSERT":
            color = "blue"
        elif status == "UPDATE":
            color = "green"
        elif status == "DELETE":
            color = "red"
        else:
            color = "gray"
        label = QLabel()
        label.setObjectName("status_label_{0}".format(id))
        label.setStyleSheet("QLabel#status_label_{0} {{background-color: {1};}}".format(id, color))
        return label

    def time_to_cook_checkbox(self, text, is_official=False):
        """Create a custom QCheckbox for every time_to_cook_item"""
        checkbox = QCheckBox()
        checkbox.setText(" {}".format(text))
        if is_official:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
        checkbox.setCheckable(False)
        return checkbox

    def set_layout(self, which_ui="Main"):
        """Set the layout of the MainWindow at startup or during use"""
        def actions_common(state):
            """Common actions for both views"""
            action_dateEdit = self.toolBar.insertWidget(self.action_Next_week, self.dateEdit)
            action_dateEdit.setVisible(True)

            self.action_View.setDisabled(state)
            if len(self.recipes) == 0:
                state = False
            self.action_Remove.setEnabled(state)
            self.action_Edit.setEnabled(state)
            if len(self.recipes) == 0:
                state = True
            self.action_Replace.setDisabled(state)
            self.action_Previous_week.setDisabled(state)
            self.action_Next_week.setDisabled(state)
            action_dateEdit.setDisabled(state)

        if which_ui == "Main":
            table = self.tableWidget_week
            actions_common(False)
            self.stackedWidget_main.setCurrentIndex(0)
            table.clearContents()
        else:
            table = self.tableWidget_view
            actions_common(True)
            self.stackedWidget_main.setCurrentIndex(1)
            table.setRowCount(0)

    def connect_actions_and_signals(self):
        """Set connections for the actions and signals not set in .ui"""
        self.action_New.triggered.connect(self.file_new)
        self.action_Open.triggered.connect(self.file_open)
        self.action_Save.triggered.connect(self.file_save)
        self.action_SaveAs.triggered.connect(lambda: self.file_save(True))
        self.action_Import.triggered.connect(self.file_import)
        self.action_Export.triggered.connect(self.file_export)
        self.action_Quit.triggered.connect(self.close)

        self.action_Add.triggered.connect(lambda: self.view_edit_dialog(edit=True, existing=False))
        self.action_Edit.triggered.connect(lambda: self.view_edit_dialog(edit=True, existing=True))
        self.action_Remove.triggered.connect(lambda: self.view_edit_dialog(edit=True, existing=False))
        self.action_Replace.triggered.connect(self.replace_row)

        self.dateEdit.dateChanged.connect(self.select_week)
        self.action_This_week.triggered.connect(lambda: self.select_week(by=0))
        self.action_View.triggered.connect(lambda: self.populate_table(which_ui="View"))
        self.action_Next_week.triggered.connect(lambda: self.select_week(by=1))
        self.action_Previous_week.triggered.connect(lambda: self.select_week(by=-1))

        self.action_Settings.triggered.connect(self.settings_dialog)

        self.comboBox_filter.currentIndexChanged.connect(self.set_recipe_filter)
        self.pushButton_select.clicked.connect(self.select_side_dish)
        self.tableWidget_view.cellClicked.connect(lambda: self.pushButton_select.setEnabled(True))
        self.tableWidget_week.doubleClicked.connect(lambda: self.set_recipe_filter(current_text=self.recipe_types["side_dish"]))

    def select_side_dish(self):
        """Select the side dish and attach it to the caller id"""
        recipe_row_num = self.tableWidget_week.currentRow()
        recipe_id = self.tableWidget_week.item(recipe_row_num, 1).text()
        side_dish_row_num = self.tableWidget_view.currentRow()
        side_dish_id = self.tableWidget_view.item(side_dish_row_num, 1).text()
        recipe_item = self.recipes[recipe_id]
        recipe_item["side_dish_id"] = side_dish_id
        recipe_item.sql_action = "UPDATE"
        self.unsaved = True
        self.pushButton_select.setVisible(False)
        self.populate_table(which_ui="Main", randomize=False)

    def set_recipe_filter(self, startup=False, current_text=None):
        """Filter the items in the table"""
        recipe_types = frozenset(self.recipe_types.values())
        if startup is True:
            current_text = "All"
            self.pushButton_select.setVisible(False)
        elif startup is False and current_text is None:
            current_text = self.comboBox_filter.currentText()
            self.pushButton_select.setVisible(False)
        elif startup is False and current_text is not None:
            # select side_dish_id
            self.comboBox_filter.setCurrentIndex(self.comboBox_filter.findText(current_text))
            self.pushButton_select.setVisible(True)
            self.pushButton_select.setEnabled(False)
        if current_text == "All":
            self.filter = recipe_types
        elif current_text in recipe_types:
            self.filter = frozenset([current_text])
        else:
            self.filter = recipe_types
        self.populate_table(which_ui="View")

    def populate_table(self, which_ui="Main", randomize=True):
        """Populate rows of the table currently shown."""
        def tables_common(table, row_num, recipe_id, recipe_item, label):
            """Common rows for the week and view tables"""
            table.setVerticalHeaderItem(row_num, QTableWidgetItem("{}".format(label)))
            time_to_cook_widget = self.time_to_cook_checkbox(recipe_item["time_to_cook"],recipe_item["exact_time_to_cook"])
            table.setItem(row_num, 1, QTableWidgetItem("{}".format(recipe_id)))
            table.setItem(row_num, 2, QTableWidgetItem(recipe_item["name"]))
            table.setItem(row_num, 3, QTableWidgetItem(recipe_item["book"]))
            table.setItem(row_num, 4, QTableWidgetItem("{}".format(recipe_item["page"])))
            table.setCellWidget(row_num, 5, time_to_cook_widget)
            if recipe_item["recipe_type"] != self.recipe_types["side_dish"]:
                side_dish_id = recipe_item["side_dish_id"]
                if side_dish_id is not None and side_dish_id in self.recipes.keys():
                    side_dish_item = self.recipes[side_dish_id]
                    table.setItem(row_num, 6, QTableWidgetItem("{}".format(side_dish_id)))
                    table.setItem(row_num, 7, QTableWidgetItem(side_dish_item["name"]))
                else:
                    cell_item = QTableWidgetItem("Select side dish")
                    cell_item.setToolTip("Doubleclick to select side dish")
                    table.setItem(row_num, 7, cell_item)

        self.set_layout(which_ui)
        if len(self.recipes) > 0:
            if which_ui == "Main":
                self.select_recipes(randomize)
                start_of_week = self.selected_date.addDays(1 - self.selected_date.dayOfWeek())
                for row_num in range(7):
                    row_date = start_of_week.addDays(row_num)
                    row_date_string = row_date.toString(self.date_string)
                    if row_date_string in self.recipe_map:
                        recipe_id = self.recipe_map[row_date_string]
                        if recipe_id is not None:
                            recipe_item = self.recipes[recipe_id]
                            if row_date == self.current_date:
                                self.tableWidget_week.setCellWidget(row_num, 0, self.status_row_label(recipe_id,"TODAY"))
                            else:
                                self.tableWidget_week.setCellWidget(row_num, 0, self.status_row_label(recipe_id,recipe_item.sql_action))
                            tables_common(self.tableWidget_week, row_num, recipe_id, recipe_item, row_date.toString("dddd\n(d.M)"))
                        else:
                            self.tableWidget_week.setItem(row_num, 1, QTableWidgetItem("No appropriate recipe"))
                            for col_num in range(2, 6):
                                self.tableWidget_week.setItem(row_num, col_num, QTableWidgetItem("N/A"))
            else:
                row_num = 0
                for recipe_id, recipe_item in self.recipes.items():
                    if recipe_item["recipe_type"] in self.filter:
                        self.tableWidget_view.insertRow(row_num)
                        self.tableWidget_view.setCellWidget(row_num, 0, self.status_row_label(recipe_id, recipe_item.sql_action))
                        tables_common(self.tableWidget_view, row_num, recipe_id, recipe_item, row_num + 1)
                        row_num += 1
                # self.tableWidget_view.sortByColumn(2, 0) # BUG: this causes items to dissapear
        else:
            self.logger((False, "Recipe list is empty. Import or add some items"))

    def select_week(self, by=0, randomize=False):
        """Go "by" weeks forward or back and repopulate table. Disable actions
        for Next and Prev week if date of expiry is hit"""
        if self.sender() is not self.dateEdit:
            if by == 0:
                self.selected_date = self.current_date
            else:
                self.selected_date = self.selected_date.addDays(by*7)
            self.dateEdit.setDate(self.selected_date)
        else:
            self.selected_date = self.dateEdit.date()

        self.populate_table(randomize=False)

        self.dateEdit.setMinimumDate(self.date_of_expiry[0])
        self.dateEdit.setMaximumDate(self.date_of_expiry[1])

        if self.date_of_expiry[0] >= self.selected_date.addDays(1 - self.selected_date.dayOfWeek()):
            self.action_Previous_week.setDisabled(True)
        else:
            self.action_Previous_week.setEnabled(True)
        if self.date_of_expiry[1] <= self.selected_date.addDays(1 - self.selected_date.dayOfWeek() + 7):
            self.action_Next_week.setDisabled(True)
        else:
            self.action_Next_week.setEnabled(True)

    def replace_row(self):
        """Clear last_cooked date of selected item and select a new one"""
        row_num = self.tableWidget_week.currentRow()
        recipe_id = self.tableWidget_week.item(row_num, 1).text()
        recipe_item = self.recipes[recipe_id]
        recipe_item["last_cooked"] = None
        recipe_item.sql_action = "UPDATE"
        self.unsaved = True
        self.populate_table(randomize=True)
        self.tableWidget_week.selectRow(row_num)

    def file_import(self):
        """Invoke the data import dialog and update the table if
        import was successfull"""
        path = "."  # TODO implement recent files
        filename = QFileDialog.getOpenFileName(self, "Import file", path, "Supported formats (%s)"
                                               % ImportExportHandler().formats())
        if filename is not None and bool(filename) is not False:
            if self.logger(self.load_data(filename, "FILE")):
                self.select_week(randomize=True)

    def file_export(self):
        """Invoke the data export dialog"""
        path = "."  # TODO implement recent files
        filename = QFileDialog.getSaveFileName(self, "Export file", path, "Supported formats (%s)"
                                               % ImportExportHandler().formats())
        if filename is not None and bool(filename) is not False:
            self.logger(self.save_data(filename, "FILE"))

    def file_open(self, startup=False):
        """If this method is invoked without argument it opens the file open
        dialog, else it tries to open the database if defined in settings"""
        path = "."  # TODO implement recent files
        if startup is False and self.can_continue():
            filename = QFileDialog.getOpenFileName(self, "Open Database", path,
                                                   "Supported formats (*.db)")
            if filename is not None and bool(filename) is not False and self.logger(self.load_data(filename, "DB")):
                self.database = filename
                self.select_week(randomize=True)
        elif startup is not False:
            if self.database is not None and self.logger(self.load_data(self.database, "DB")):
                self.select_week(randomize=True)
            elif self.database is None:
                self.select_week(randomize=False)

    def file_new(self):
        """Clear recipe list"""
        if self.can_continue():
            self.recipes.clear()
            self.select_week(randomize=False)

    def file_save(self, saveas=False):
        """Save recipes list into database"""
        path = "."  # TODO implement recent files
        if saveas is False and self.database is not None:
            output = self.logger(self.save_data(self.database, "DB"))
        else:
            filename = QFileDialog.getSaveFileName(self, "Save to database", path,
                                                   "Supported formats (*.db)")
            if filename is not None and bool(filename) is not False:
                self.database = filename
                output = self.logger(self.save_data(self.database, "DB"))
            else:
                output = False
        if output:
            self.unsaved = False
            self.populate_table(randomize=False)
            return True
        else:
            return False

    def view_edit_dialog(self, edit=False, existing=False):
        """Opens a dialog to edit currently selected row or view all recipes"""
        self.set_layout("Viewer")
        self.stackedWidget_main.setCurrentIndex(1)
        #if not edit:
            #dialog = Qhar_View(edit=False, item_id=None)
        #else:
            #if not existing:
                ## add new item
                #dialog = Qhar_View(edit=True, item_id=None)
            #else:
                ## edit selected item
                #dialog = Qhar_View(edit=True, item_id="123")
        #dialog.exec_()

    def logger(self, ret):
        """Display messages in statusbar and log widget, also passtrough
        True or False statuses: useful for if statements."""
        if ret is not None:
            if type(ret) is str:
                status, msg = None, ret
            elif len(ret) == 1:
                status, msg = None, ret
            elif len(ret) == 2:
                status, msg = ret
            self.statusBar().showMessage(msg)
            self.listWidget_log.addItem(msg)
        else:
            status = False
        return status

    def closeEvent(self, event):
        """On closing the MainWindow this method tries to save any unsaved changes
        before exiting the program"""
        if self.can_continue():
            self.save_settings()
            event.accept()
        else:
            event.ignore()

    def can_continue(self):
        """This method checks if recipe list contains unsaved changes and
        provides a propmpt to save them."""
        if self.unsaved:
            reply = QMessageBox.question(self, "Qhar - Unsaved Changes", "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.file_save()
        return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Andrej Mernik")
    app.setOrganizationDomain("mernik.eu")
    app.setApplicationName("Qhar")
    window = Qhar_MainWindow()
    window.show()
    app.exec_()