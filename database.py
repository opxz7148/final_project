# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os
import copy


# add in code for a Database class
class Database:
    def __init__(self, name):
        """
        Construct database class by setting database name and create db list to contain table in the future
        :param name: Name of the database
        """
        self.name = name
        self.db = []

    def insert_table(self, table):
        """
        function to insert new data table into database.
        :param table: Table object
        """
        if isinstance(table, Table):
            self.db.append(table)
        else:
            raise ValueError("Table to insert in to be instance of Table class")

    def search(self, table_name):
        """
        funtion to find certain table in database by name of table
        :param table_name: name of table that user want to search.
        :return: Table instance or none
        """
        for table in self.db:
            if table.table_name == table_name:
                return table
        print("Table not found.")
        return None

    def add_csv_table(self, filename):
        """
        Import new dataset from csv file and add to database
        :param filename: Name of csv file that user want to add to database
        :return:
        """
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        lst = []
        with open(os.path.join(__location__, filename)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                lst.append(dict(r))
        self.insert_table(Table(filename, lst))

# add in code for a Database class

# add in code for a Table class
class Table:
    def __init__(self, name, dict_lst):
        """
        Construct a table class to contain data in list of dict format
        :param name: String name of table
        :param dict_lst: List of dictionaries
        """
        self.table_name = name
        self.table = dict_lst

    def insert(self, info):
        """
        Use to insert new set of information into a table as dict format.
        :param info: dictionaries of information
        """
        if isinstance(info, dict):
            self.table.append(info)

    def __floatable(self, element):
        """
        Internal function to check is certain information are able to convert to float or not.
        :param element: Element that user want to check
        """
        if element is None:
            return False

        try:
            float(element)
            return True

        except ValueError:
            return False

    def join(self, other_table, common_key):
        """
        Function to join other table then return a new table that combine both table with common key that user want to filter.
        :param other_table: Other Table instance
        :param common_key: Key that user want to include in new table
        :return:
        """
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)

        return joined_table

    def filter(self, condition, new_name=""):
        """
        Function to filter table with certain condition
        :param condition: Condition that user want to filter as a lambda function
        :return: New table instance that already filtered.
        """
        if new_name == "":
            filtered_table = Table(self.table_name + '_filtered', [])
        else:
            filtered_table = Table(new_name, [])

        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        """
        Function to gather certain information and do some calculation with it
        :param function: Function that user want to do with list of information.
        :param aggregation_key: Key of information that user want to work with.
        :return: Result of function
        """
        temps = []
        for item1 in self.table:
            if self.__floatable(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def print_table(self, exclude_key="", new_line_key=""):
        """
        Function too print out table with easy to read format.
        """
        key_ls = []
        for key in list(self.table[0].keys()):
            if key in exclude_key or key in new_line_key:
                continue
            else:
                key_ls.append(key)

        column_size = 30
        table_size = (column_size * len(key_ls) + len(key_ls) + 1)
        print("-" * table_size)

        print(f"| {'Table name : ' + self.table_name:^30}", end="")
        print(" " * (table_size - len('| Table name:' + self.table_name) - 3), end="")
        print("|")

        print("-" * table_size)

        print("|", end="")

        for key in key_ls:
            print(f"{key:^30}", end="|")
        print()

        for item in self.table:

            print("-" * table_size)
            print("|", end="")
            for key in key_ls:
                print(f"{item[key]:^30}", end="|")
            print("")

            for new_line in new_line_key:
                print("-" * table_size)
                print(f"| {new_line}: {item[new_line]}", end="")
                print(" " * (table_size - len(new_line) - len(item[new_line]) - 5), end="")
                print("|")


        print("-" * table_size)

# mydb = Database("db1")
# mydb.add_csv_table("persons.csv")
# person_table = mydb.search("persons.csv")
# person_table.print_table()
# person_table.insert({'ID': '1111111', 'fist': 'Ohm', 'last': 'S.', 'type': 'student'})
# person_table.print_table()
#
