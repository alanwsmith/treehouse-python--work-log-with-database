"""Worklog with a database back end
"""

from peewee import *

import re

database_connection = SqliteDatabase(None)


class Task(Model):
    employee = CharField()
    task = CharField()
    notes = CharField()
    date = DateField()

    class Meta:
        database = database_connection

class Worklog:

    def __init__(self):
        self.db = database_connection 

    def add_task(self, params):
        """Add an entry to the database

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "notes": "Good stuff here", "date": "2017-01-01"})
        >>> Task.select().count()
        1

        """
        new_task = Task.create(**params)
        new_task.save()

    def ask_for_input(self):
        """Generic method to gather user input to
        pass on to other methods for validaiton.
        """
        return input("> ").strip()

    def build_database_tables(self):
        """Create the actual database tables

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True

        """

        self.db.create_tables([Task], safe=True) 
        return Task.table_exists()


    def clear_screen(self):
        """Convience method for clearing the screen
        """
        print("\033c", end="")


    def connect_to_database(self, database_name):
        """Make the database connection

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.db.is_closed()
        False

        """ 

        self.db.init(database_name)
        self.db.connect()

    def display_main_prompt(self):
        """This is the top level prompt for the interface.

        >>> wl = Worklog()
        >>> wl.display_main_prompt()
        1. Add a new task.
        2. Lookup tasks.

        """

        print("1. Add a new task.")
        print("2. Lookup tasks.")


    def get_list_of_employees(self):
        """Return a list of the employees in the database

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> employee_list = wl.get_list_of_employees()
        >>> employee_list[0]
        'Alex'

        """

        employees = []

        for task in Task.select():
            employees.append(task.employee)

        employees.sort()

        return employees 


    def get_new_entry_data(self):
        print("What is your name?")
        name = self.ask_for_input() 
        print("What is the name of your task?")
        task = self.ask_for_input() 
        print("How long did you spend on it?")
        time_spent = self.ask_for_input() 
        print("Add more notes here or just hit Enter/Return to continue")
        notes = self.ask_for_input() 
        # TODO: Validate each item above
        # TODO: Send to database after validation.

    def how_to_find_previous_entries_prompt(self):
        """Prompt for how to search for previous entries

        >>> wl = Worklog()
        >>> wl.how_to_find_previous_entries_prompt()
        'How do you want to find previous entries?\\n1 = By Employee\\n2 = By Date\\n3 = By Search Term'

        """
        return "How do you want to find previous entries?\n1 = By Employee\n2 = By Date\n3 = By Search Term"
        

    def validate_main_prompt_input(self, test_string):
        """Make sure a value of '1' or '2' was passed

        >>> wl = Worklog()
        >>> wl.validate_main_prompt_input("1")
        True
        >>> wl.validate_main_prompt_input("2")
        True
        >>> wl.validate_main_prompt_input("asdfasdf")
        False

        """
        pattern = re.compile("^(1|2)$")
        if pattern.match(test_string):
            return True 
        else:
            return False

    def validate_how_to_find_previous_entries_prompt(self, test_string):
        """Make sure the value passed is either a 1, 2, or 3

        >>> wl = Worklog()
        >>> wl.validate_how_to_find_previous_entries_prompt("1")
        True
        >>> wl.validate_how_to_find_previous_entries_prompt("2")
        True
        >>> wl.validate_how_to_find_previous_entries_prompt("3")
        True
        >>> wl.validate_how_to_find_previous_entries_prompt("invalid value")
        False

        """

        pattern = re.compile("^[1-3]$")
        if pattern.match(test_string):
            return True
        else:
            return False



if __name__ == "__main__":
    import doctest
    if doctest.testmod().failed:
        print("--- Tests Failed ---")
    else:
        wl = Worklog()
        print("What would you like to do?") 
        wl.display_main_prompt()
        check_input = wl.ask_for_input()
        while not wl.validate_main_prompt_input(check_input):
            wl.clear_screen()
            print("You must choose either 1 or 2.")
            wl.display_main_prompt()
            check_input = wl.ask_for_input()

        if check_input == "1":
            print("Adding new item")
        else:
            print("Looking up")




        # wl.ask_for_input()
        # wl.get_new_entry_data()


