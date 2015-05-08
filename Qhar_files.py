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

import csv
import sqlite3
import os.path
from PyQt4.QtCore import *
from Qhar_settings import *


class DatabaseHandler(Settings):
    def __init__(self, filename=None, contents=None):
        super(DatabaseHandler, self).__init__()
        self.__filename = filename
        self.__contents = contents

    def __iter__(self):
        if self.__contents is None:
            # read
            return self.load_database()
        else:
            # write
            return self.save_database()

    def check_database_structure(self):
        """Check if the database we are writing in/reading from has correct
        structure (e.g. it has all columns our program uses)"""
        db = None
        try:
            db = sqlite3.connect(self.__filename)
            db.row_factory = sqlite3.Row
            row = db.execute("PRAGMA table_info({0})".format(self.table_name))
            table_structure = frozenset([item["name"] for item in row])
            if frozenset(self.arguments.keys()).issubset(table_structure):
                return True
            else:
                return False
        except Exception:
            return False
        finally:
            if db is not None:
                db.close()

    def dict_factory(self, cursor, row):
        """This method is used to return db result as a dictionary"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def load_database(self):
        """Try to load the database (if it exists and populate the self.recipes
        list. Return message upon/success failure"""
        if not QFileInfo(self.__filename).exists():
            yield False, "No such database, loading aborted."
        elif not self.check_database_structure():
            yield False, "Database corrupt, loading aborted."
        else:
            db = None
            try:
                db = sqlite3.connect(self.__filename)
                db.row_factory = self.dict_factory
                for dict_result in db.execute("SELECT * FROM {0}".format(self.table_name)):
                    yield dict_result
            except Exception:
                yield False, "Something went wrong when loading the database."
            finally:
                if db is not None:
                    db.close()

    def save_database(self):
        """This method saves the data into the database. It's used to insert/update
        and delete records. """
        if not QFileInfo(self.__filename).exists():
            if not self.create_database():
                yield False, "Could not create database, saving aborted."
        if QFileInfo(self.__filename).exists():
            if not self.check_database_structure():
                yield False, "Database corrupt, saving aborted."
            elif len(self.__contents) == 0:
                yield False, "Nothing to save."
            else:
                db = None
                try:
                    db = sqlite3.connect(self.__filename)
                    for item in self.__contents.values():
                        if item.create_sql is not None:
                            db.execute(item.create_sql)
                    db.commit()
                    yield True, "Saving was successfull"
                except KeyError:
                    yield False, "Saving to database failed!"
                finally:
                    if db is not None:
                        db.close()

    def create_database(self):
        """This method creates a database if the file doesn't exist yet"""
        db = None
        try:
            db = sqlite3.connect(self.__filename)
            sql = ", ".join(["{0} {1}".format(key, val) for key, val in self.db_types.items()])
            db.execute("CREATE TABLE {0} (id INTEGER PRIMARY KEY, {1})".format(self.table_name, sql))
            db.commit()
            return True
        except Exception:
            return False
        finally:
            if db is not None:
                db.close()


class ImportExportHandler(Settings):
    def __init__(self, filename=None, contents=None):
        super(ImportExportHandler, self).__init__()
        self.__filename = "{0}".format(filename)
        self.__contents = contents

    def __iter__(self):
        if self.__contents is not None:
            # write
            if os.path.splitext(self.__filename)[1] == ".csv":
                return self.write_csv()
        else:
            # read
            if os.path.splitext(self.__filename)[1] == ".csv":
                return self.read_csv()

    @staticmethod
    def formats():
        return "*.csv"

    def read_csv(self):
        """This method reads the CSV file one line at at time"""
        csvfile = None
        required_arguments = frozenset([value for key, value in self.arguments.items()
                                        if self.arguments_required[key] is True])
        optional_arguments = frozenset([value for key, value in self.arguments.items()
                                        if self.arguments_required[key] is False])
        try:
            with open(self.__filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                header = next(csv_reader)
                if not required_arguments.issubset(frozenset(header)):
                    yield False, "Invalid header in CSV file"
                else:
                    header_map = dict()
                    for num, item in enumerate(header):
                        if item in optional_arguments or item in required_arguments:
                            header_map[item.lower().replace(" ", "_")] = num
                for item in csv_reader:
                    output = dict()
                    for map_key, map_value in header_map.items():
                        # drop empty cells
                        if len(item[map_value]) > 0:
                            output[map_key] = item[map_value]
                    yield output
        except Exception:
            yield False, "Failed to load CSV file"
        finally:
            if csvfile is not None:
                csvfile.close()

    def write_csv(self):
        """This method writes the recipes list into a CSV file"""
        csvfile = None
        header = {argument.lower().replace(" ", "_"): argument for argument in
                  self.required_arguments+self.optional_arguments}
        argument_list = header.keys()
        if len(self.__contents) == 0:
            yield False, "Nothing to export."
        try:
            with open(self.__filename, "wb") as csvfile:
                w = csv.DictWriter(csvfile, argument_list,
                                   delimiter='\t', quotechar='|')
                num = 0
                w.writerow(header)
                for val in self.__contents.values():
                    w.writerow(val.__dict__())
                    num += 1
            yield True, "Exported {0} recipes".format(num)
        except:
            yield False, "Failed to write CSV file"
        finally:
            if csvfile is not None:
                csvfile.close()