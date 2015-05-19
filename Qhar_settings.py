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


class Settings(object):
    """This object holds information about the arguments, types and lenghts of
    data used in this program. It also provides methods to load/save settings"""
    def __init__(self):
        super(Settings, self).__init__()
        self.table_name = "recipes"
        self.arguments = {"name": "Name",
                          "book": "Book",
                          "page": "Page",
                          "time_to_cook": "Time to cook",
                          "exact_time_to_cook": "Exact time to cook",
                          "recipe_type": "Recipe type",
                          "last_cooked": "Last cooked",
                          "side_dish_id": "Side dish ID"}
        self.db_types = {"name": "VARCHAR",
                         "book": "VARCHAR",
                         "page": "INT",
                         "time_to_cook": "INT",
                         "exact_time_to_cook": "BOOLEAN",
                         "recipe_type": "VARCHAR",
                         "last_cooked": "DATE",
                         "side_dish_id": "VARCHAR"}
        self.arguments_required = {"name": True,
                                   "book": True,
                                   "page": True,
                                   "time_to_cook": False,
                                   "exact_time_to_cook": False,
                                   "recipe_type": False,
                                   "last_cooked": False,
                                   "side_dish_id": False}
        self.current_date = QDate().currentDate()
        self.date_of_expiry = (self.current_date.addDays(1 - self.current_date.dayOfWeek() - 14),
                               self.current_date.addDays(1 - self.current_date.dayOfWeek() + 14))
        self.selected_date = self.current_date
        self.date_string = "dd.MM.yyyy"
        self.available_time = [60, 60, 60, 60, 60, 120, 120]
        self.recipe_types = {"one_course_meal": "Samostojna jed",
                             "side_dish": "Priloga",
                             "main_course_with_meat": "Mesna jed",
                             "main_course_with_vegetables": "Zelenjavna jed",
                             "soup": "Juha"}
        self.database = None

    def load_settings(self):
        """This method tries to load settings from the default save location
        in .config"""
        settings = QSettings()
        if settings.value("FirstRun") is not None:  
            self.restoreGeometry(settings.value("MainWindow/Geometry"))
            self.restoreState(settings.value("MainWindow/State"))
            self.window_size = settings.value("MainWindow/Size", QSize(600, 500))
            self.resize(self.window_size)

            """The following values are saved into the recipe container"""
            available_time = settings.value("Configuration/AvailableTime")
            database = settings.value("Configuration/Database")

            if available_time is not None:
                self.available_time = [int(item) for item in available_time]
            if database is not None and QFileInfo(database).exists():
                self.database = database

    def save_settings(self):
        """This method gets executed after after the MainWindow is closed or if
        the user clicks the settings dialog"""
        settings = QSettings()
        settings.setValue("FirstRun", "0")
        
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())
        settings.setValue("MainWindow/Size", self.size())

        if self.available_time is not None:
            settings.setValue("Configuration/AvailableTime", self.available_time)
        if self.database is not None:
            settings.setValue("Configuration/Database", self.database)
            
    def settings_dialog(self):
        """Display settings dialog"""
        pass