#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Qhar_view_ui import *
from Qhar_data import *


class Qhar_View(RecipeContainer, QDialog, Ui_Qhar_ViewerEditor):
    def __init__(self, edit, item_id):
        super(Qhar_View, self).__init__()
        self.edit = edit
        self.item_id = item_id
        self.table_map = dict()
        self.setupUi(self)
        self.create_items()
        self.set_layout()
        self.connect_actions_and_signals()
        self.viewer("all")
        if self.edit:
            self.Qhar_ViewEdit.setCurrentWidget(self.Qhar_edit)
            self.editor()
        else:
            self.Qhar_ViewEdit.setCurrentWidget(self.Qhar_view)
    
    def create_items(self):
        """Create items which which were not created with Qt designer"""
        self.label_Book.setText("Book")
        self.label_Filter.setText("Filter")
        self.label_LastCooked.setText("Last cooked")
        self.label_Name.setText("Name")
        self.label_Page.setText("Page")
        self.label_RecipeType.setText("Recipe type")
        self.label_TimeToCook.setText("Time to Cook")
        self.checkBox_ExactTimeToCook.setText("Exact time?")
  
        self.Qhar_ViewEdit.setTabText(0, "View");        
        self.Qhar_ViewEdit.setTabText(0, "Add");        
        
        self.pushButton_Add.setText("Add")
        self.pushButton_Close.setText("Close")
        self.pushButton_Cancel.setText("Cancel")
        self.pushButton_Edit.setText("Edit")
        self.pushButton_Save.setText("Save")

    def set_layout(self):
        """Set the layout of the Dialog at start"""
    
    def connect_actions_and_signals(self):
        """Set connections for the actions and signals not set in .ui"""

    def editor(self):
        if self.item_id is None: 
            self.Qhar_ViewEdit.setTabText(1, "Add");
            self.pushButton_Save.setText("Add")
            self.pushButton_Save.setIcon(QIcon.fromTheme("list-add"))
          
    def viewer(self, recipe_type):
        """Fill table with items from recipes list"""
        if recipe_type == "all":
            recipe_types = frozenset(self.recipe_types)
        else:
            recipe_types = frozenset([recipe_type])
        for recipe_item in self.recipes.items():
            print(recipe_item)
            if recipe_item["recipe_type"] in recipe_types:
                recipe_id = hash(recipe_item)
                row_num = self.tableViewWidget.insertRow()
                self.tableViewWidget.setItem(row_num, 1, QTableWidgetItem(recipe_item["name"]))
                self.tableViewWidget.setItem(row_num, 2, QTableWidgetItem(recipe_item["book"]))
                self.tableViewWidget.setItem(row_num, 3, QTableWidgetItem("{}".format(recipe_item["page"])))
                self.tableViewWidget.setItem(row_num, 4, QTableWidgetItem("{}".format(recipe_item["time_to_cook"])))
                # Main dish ID
                self.tableViewWidget.setItem(row_num, 6, QTableWidgetItem("{}".format(recipe_id)))
                # Side dish ID
                side_dish_id = recipe_item["side_dish_id"]
