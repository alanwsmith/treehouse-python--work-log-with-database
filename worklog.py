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

    def display_add_task_prompt(self):
        """Show the initial add task_prompt

        >>> wl = Worklog()
        >>> wl.display_add_task_prompt()
        What is the name of the employee who performed the task?

        """
        print("What is the name of the employee who performed the task?")


    def display_date_prompt(self):
        """Prompt for the date

        >>> wl = Worklog()
        >>> wl.display_date_prompt()
        What date was the task performed (format: YYYY-MM-DD)?

        """
        print("What date was the task performed (format: YYYY-MM-DD)?")


    def display_main_prompt(self):
        """This is the top level prompt for the interface.

        >>> wl = Worklog()
        >>> wl.display_main_prompt()
        1. Add a new task
        2. Lookup tasks
        3. Quit

        """

        print("1. Add a new task")
        print("2. Lookup tasks")
        print("3. Quit")

    def display_name_of_task_prompt(self):
        """Ask for the name of the task

        >>> wl = Worklog()
        >>> wl.display_name_of_task_prompt()
        What task was done?

        """

        print("What task was done?")



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
        >>> wl.validate_main_prompt_input("3")
        True
        >>> wl.validate_main_prompt_input("asdfasdf")
        False

        """
        pattern = re.compile("^[1-3]$")
        if pattern.match(test_string):
            return True 
        else:
            return False

    def validate_name(self, name):
        """Make sure the name is valid. 

        Letters, spaces, and periods are allowed. 
        
        >>> wl = Worklog()
        >>> wl.validate_name("Bob")
        True
        >>> wl.validate_name("A")
        True
        >>> wl.validate_name("Alan W. Smith")
        True
        >>> wl.validate_name("")
        False
        >>> wl.validate_name("Alan1")
        False

        """

        pattern = re.compile("^[a-zA-Z\s\.]+$")
        if pattern.match(name):
            return True
        else:
            return False

    def validate_task(self, task):
        """Make sure the task is a valid string

        >>> wl = Worklog()
        >>> wl.validate_task("Did something")
        True
        >>> wl.validate_task("Made something with numbers 1235")
        True
        >>> wl.validate_task("")
        False

        """

        if task != "":
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

        print("--- Tests Passed ---")
        # exit()

        wl = Worklog()
        wl.clear_screen()
        print("What would you like to do?") 
        wl.display_main_prompt()
        check_input = wl.ask_for_input()
        while not wl.validate_main_prompt_input(check_input):
            wl.clear_screen()
            print("That wasn't a valid option. Try again.")
            wl.display_main_prompt()
            check_input = wl.ask_for_input()

        if check_input == "1":
            wl.clear_screen()
            wl.display_add_task_prompt()
            employee = wl.ask_for_input()
            while not wl.validate_name(employee):
                wl.clear_screen()
                print("Names can only contain letters, spaces, and periods.")
                print("Names also cannot be empty. Try again.")
                employee = wl.ask_for_input()

            wl.clear_screen()
            wl.display_name_of_task_prompt()
            task = wl.ask_for_input()
            while not wl.validate_task(task):
                wl.clear_screen()
                print("The task can't be empty. Try again.")
                task = wl.ask_for_input()

            wl.clear_screen()





        elif check_input == "2":
            print("Looking up")
        else:
            print("Quitting")


    # TODO: Test everything with an empty database too.

