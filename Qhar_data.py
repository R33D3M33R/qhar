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
from Qhar_files import *
from random import shuffle
from Qhar_settings import Settings
import hashlib


class RecipeItem(Settings):
    """"This class is used to store the recipe item. It also serves to
    check the items before adding them to recipe list"""
    # TODO convert class to proper dict
    # TODO evaluate arguments @ __setitem__
    # TODO __iter__, __contains__ ...
    def __init__(self, values=None, sql_action=None):
        super(RecipeItem, self).__init__()
        self.__valid = True
        self.__sql_action = sql_action
        self.values = values
        self.__valid = self.check_values("all")

    def check_values(self, which):
        """This method serves to validate values. If which = all, all checks are performed,
        else, only check for value_name = which get checked to save time."""
        try:
            if self.values is None:
                raise ValueError

            # arguments
            for key, value in self.arguments_required.items():
                if value and key not in self.values:
                    raise ValueError
                elif not value and key not in self.values:
                    self.values[key] = None
                else:
                    self.values[key] = self.value_convert(key)

            # errors in required arguments are fatal
            if self.values["name"] is None or self.values["book"] is None:
                raise ValueError
            if self.values["page"] < 0:
                raise ValueError
            self.__required = {key: self.values[key] for key, value in
                               self.arguments_required.items() if value}

            # validation of optional arguments
            if self.values["recipe_type"] is None or self.values["recipe_type"] not in self.recipe_types.values():
                self.values["recipe_type"] = self.recipe_types["one_course_meal"]

            if self.values["time_to_cook"] is None:
                self.values["time_to_cook"] = 60

            if self.values["last_cooked"] is not None:
                date_last_cooked = self.values["last_cooked"]
                if date_last_cooked < self.date_of_expiry[0]:
                    # recipe has expired
                    self.values["last_cooked"] = None
                elif date_last_cooked >= self.date_of_expiry[0]:
                    if self.__sql_action == "DELETE":
                        # recipe hasn't expired, but it's set for deletion
                        self.values["last_cooked"] = date_last_cooked.addYears(1).toString(self.date_string)
                    else:
                        # QDate isn't hashable, but string is
                        self.values["last_cooked"] = date_last_cooked.toString(self.date_string)
                else:
                    self.values["last_cooked"] = None
            return True
        except ValueError:
            return False

    def value_convert(self, key):
        """Convert self.values[key] to datatype given in db_types"""
        if self.values[key] is not None:
            try:
                if self.db_types[key] == "BOOLEAN":
                    if self.values[key] is True:
                        return True
                    else:
                        return False
                elif self.db_types[key] == "INT":
                    return int(self.values[key])
                elif self.db_types[key] == "DATE":
                    date_string = QDate.fromString(self.values[key], self.date_string)
                    if date_string.isValid():
                        return date_string
                    else:
                        raise ValueError
                else:
                    if len(str(self.values[key])) > 0:
                        return str(self.values[key])
                    else:
                        raise ValueError
            except Exception:
                return None
        else:
            return None

    @property
    def sql_action(self):
        return self.__sql_action

    @sql_action.setter
    def sql_action(self, action):
        self.__sql_action = action

    @property
    def is_valid(self):
        return self.__valid

    @property
    def create_sql(self):
        """This property returns the sql statement depending on the sql_action
        value (INSERT, DELETE or UPDATE). It defaults to None (do nothing)."""
        if self.__sql_action == "INSERT":
            form1 = ", ".join(["{0}".format(key) for key in self.values.keys()])
            form2 = ", ".join([self.quote_val(val) for val in self.values.values()])
            return "INSERT into {0} ({1}) VALUES ({2})".format(self.table_name, form1, form2)
        elif self.__sql_action == "DELETE":
            form1 = " AND ".join(["{0}={1}".format(key, self.quote_val(value))
                                  for key, value in self.__required.items()])
            return "DELETE FROM {0} WHERE {1}".format(self.table_name, form1)
        elif self.__sql_action == "UPDATE":
            form1 = ",".join(["{0}={1}".format(key, self.quote_val(value))
                              for key, value in self.values.items()])
            form2 = " AND ".join(["{0}={1}".format(key, self.quote_val(value))
                                  for key, value in self.__required.items()])
            return "UPDATE {0} SET {1} WHERE {2}".format(self.table_name, form1, form2)
        else:
            return None

    def quote_val(self, s):
        """Return quoted empty string if input is None else quoted string"""
        if s is None:
            return "''"
        return "'"+str(s)+"'"

    def __eq__(self, other):
        return frozenset(self.__required.values()) == frozenset(other.__required.values())

    def sha1_hex(self):
        string = "|".join(sorted(str(item) for item in self.__required.values()))
        return hashlib.sha1(string.encode('utf-8')).hexdigest()

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __dict__(self):
        return self.values


class RecipeContainer(Settings):
    """This class is used to handle calls from dialogs of the MainWindow"""
    def __init__(self):
        super(RecipeContainer, self).__init__()
        self.recipes = dict()
        self.__unsaved = False

    @property
    def unsaved(self):
        return self.__unsaved

    @unsaved.setter
    def unsaved(self, value):
        if value:
            value = True
        else:
            value = False
        self.action_Save.setEnabled(value)
        self.action_SaveAs.setEnabled(value)
        self.__unsaved = value

    # import/export
    def load_data(self, filename, handler):
        """This method imports data into recipes list. handler is either DB
        for database or FILE for file export. Loading from database clears
        previous data."""
        if handler == "DB":
            handle = DatabaseHandler(filename, None)
            self.recipes.clear()
        else:
            handle = ImportExportHandler(filename, None)
        num = 0
        for item in handle:
            if type(item) is not dict:
                return item
            else:
                if handler == "DB":
                    recipe = RecipeItem(item, None)
                else:
                    recipe = RecipeItem(item, "INSERT")

                if recipe.is_valid:
                    if self.add_recipe(recipe):
                        num += 1
        if num > 0:
            if handler != "DB":
                self.unsaved = True
                return True, "Imported {0} new recipes".format(num)
            else:
                self.unsaved = False
                return True, "Loaded {0} recipes from database".format(num)
        else:
            if handler != "DB":
                return False, "No new recipes imported"
            else:
                return False, "No recipes were loaded"

    def save_data(self, filename, handler):
        """This method exports data from recipes list. handler is either DB
        for database or FILE for file export."""
        if handler == "DB":
            handle = DatabaseHandler(filename, self.recipes)
        else:
            handle = ImportExportHandler(filename, self.recipes)
        for item in handle:
            if item:
                # data was saved, cleanup recipe list
                self.cleanup_recipe_list()
            return item

    # recipe manipulation
    def add_recipe(self, recipe):
        """Mark recipe for insertion and perform the action"""
        recipe_hash = recipe.sha1_hex()
        if recipe_hash not in self.recipes.keys():
            self.recipes[recipe_hash] = recipe
            return True
        else:
            return False

    # cleanup the recipe list
    def cleanup_recipe_list(self):
        """Cleanup the recipe list by removing sql_action UPDATE and INSERT and
        deleting the items with sql_action DELETE"""
        for recipe_id, recipe_item in self.recipes.items():
            if recipe_item.sql_action == "DELETE":
                del self.recipes[recipe_id]
            else:
                print(recipe_item.sql_action)
                recipe_item.sql_action = None
                print(recipe_item.sql_action)

    def update_recipe(self, recipe_hash, recipe):
        """This method updates a recipe already in recipes list if the hash is
        unchanged. If hash has changed, run both delete_recipe[oldhash] and
        add_recipe[newhash] instead"""
        pass

    def delete_recipe(self, recipe_hash):
        """This method marks recipe from recipes list for deletion"""
        pass

    def select_recipes(self, randomize=True):
        """Invoking this method populates the table with items from the recipes
        list. First all items with last_cooked set are connected regardles of
        avaliable time."""
        self.recipe_map = dict.fromkeys([self.current_date.addDays(day).toString(self.date_string)
                                         for day in range(self.date_of_expiry[0].dayOfYear() - self.current_date.dayOfYear(),
                                                          self.date_of_expiry[1].dayOfYear() - self.current_date.dayOfYear())])

        recipes_inverted = {val["last_cooked"]: key for key, val in self.recipes.items()
                            if val["last_cooked"] is not None}
        self.recipe_map.update(recipes_inverted)
        recipes_randomized = [[key, val["time_to_cook"]] for key, val in
                              self.recipes.items() if
                              val["last_cooked"] is None and
                              val["recipe_type"] != self.recipe_types["side_dish"]]
        shuffle(recipes_randomized)
        for key, value in self.recipe_map.items():
            if value is None:
                available_time = self.available_time[QDate.fromString(key, self.date_string).dayOfWeek()-1]
                # select first item from recipes_randomized which is in time_to_cook
                for num, row in enumerate(recipes_randomized):
                    if row[1] <= available_time+30 and row[1] >= available_time-30:
                        # update recipe_map, update_recipe, break loop
                        self.recipe_map[key] = row[0]
                        self.recipes[row[0]]["last_cooked"] = key
                        self.recipes[row[0]].sql_action = "UPDATE"
                        self.unsaved = True
                        del recipes_randomized[num]
                        break

    def __len__(self):
        return len(self.recipes)