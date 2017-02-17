"""Worklog with a database back end
"""

from peewee import *
from time import gmtime, strftime

import re

database_connection = SqliteDatabase(None)


class Task(Model):
    date = DateField()
    employee = CharField(max_length=255)
    minutes = IntegerField()
    notes = TextField()
    task = CharField(max_length=255)

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
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 10, "notes": "Good stuff here", "date": "2017-01-01"})
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

    def display_date_selection_prompt(self, dates):
        """Show the date selection menu

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> dates = wl.get_list_of_dates()
        >>> wl.display_date_selection_prompt(dates)
        Choose a date:
        1. 2016-10-21
        2. 2017-01-01
        """

        print("Choose a date:")
        for date_index, date in enumerate(dates):
            print("{}. {}".format(int(date_index) + 1, date))


    def display_employee_name_prompt(self):
        """Show the initial add task_prompt

        >>> wl = Worklog()
        >>> wl.display_employee_name_prompt()
        Who did the task (e.g. Bob)?
         

        """
        print("Who did the task (e.g. Bob)?")

    def display_employee_selection_prompt(self, employee_array):
        """Print list of the employees. 

        >>> wl = Worklog()
        >>> wl.display_employee_selection_prompt(["Alex", "Bob"])
        Which employee do you want to review:
        1. Alex
        2. Bob

        """
        print("Which employee do you want to review:")
        for employee_index, employee in enumerate(employee_array):
            print("{number}. {name}".format(number=employee_index + 1, name=employee))


    def display_lookup_prompt(self):
        """Ask how the user wants to lookup entries. 

        >>> wl = Worklog()
        >>> wl.display_lookup_prompt()
        How do you want to lookup entires:
        1. By Employee
        2. By Date
        3. By Search Term

        """
        print("How do you want to lookup entires:")
        print("1. By Employee")
        print("2. By Date")
        print("3. By Search Term")


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

    def display_minutes_prompt(self):
        """Ask for how many minutes were spent on the task

        >>> wl = Worklog()
        >>> wl.display_minutes_prompt()
        How many minutes did you spend on the task?

        """

        print("How many minutes did you spend on the task?")


    def display_name_of_task_prompt(self):
        """Ask for the name of the task

        >>> wl = Worklog()
        >>> wl.display_name_of_task_prompt()
        What task was done (e.g. Updated database)?

        """

        print("What task was done (e.g. Updated database)?")

    def display_notes_prompt(self):
        """Ask for optional notes

        >>> wl = Worklog()
        >>> wl.display_notes_prompt()
        Enter notes about the task, or just hit Enter/Return to skip them:

        """

        print("Enter notes about the task, or just hit Enter/Return to skip them:")

    def display_search_prompt(self):
        """Ask for the search term

        >>> wl = Worklog()
        >>> wl.display_search_prompt()
        What term would you like to search for?

        """

        print("What term would you like to search for?")


    def get_list_of_dates(self):
        """Return a list of the dates in the database

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.get_list_of_dates()
        [datetime.date(2016, 10, 21), datetime.date(2017, 1, 1)]
        """

        dates = []

        for task in Task.select():
            dates.append(task.date)

        dates = list(set(dates))
        dates.sort()

        return dates


    def get_list_of_employees(self):
        """Return a list of the employees in the database

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> employee_list = wl.get_list_of_employees()
        >>> employee_list[0]
        'Alex'
        >>> employee_list[1]
        'Bob'

        """

        employees = []

        for task in Task.select():
            employees.append(task.employee)

        unique_list_of_employees = list(set(employees))
        unique_list_of_employees.sort()

        return unique_list_of_employees


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

    def get_tasks_for_date(self, date_number):
        """Return the tasks for a given date.

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> tasks = wl.get_tasks_for_date(2)
        >>> tasks[0]["task"]
        'Make stuff'
        >>> tasks[0]["employee"]
        'Bob'

        """

        date_list = self.get_list_of_dates()
        date_index = int(date_number) - 1
        date_string = date_list[date_index]

        tasks = []

        for task_item in Task.select().where(Task.date== date_string):
            tasks.append({
                "task": task_item.task, 
                "employee": task_item.employee, 
                "minutes": task_item.minutes,
                "date": task_item.date,
                "notes": task_item.notes
            })

        return tasks 
        

    def get_tasks_for_employee(self, employee_number):
        """Return the tasks for a given emplyee.

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> tasks = wl.get_tasks_for_employee("2")
        >>> tasks[0]["task"]
        'Make stuff'
        >>> tasks = wl.get_tasks_for_employee("1")
        >>> tasks[0]["task"]
        'Alex top task'
        >>> tasks[1]["task"]
        'Another task'
        >>> tasks[1]["employee"]
        'Alex'
        >>> tasks[1]["minutes"]
        30
        >>> tasks[1]["date"]
        datetime.date(2016, 10, 21)
        >>> tasks[1]["notes"]
        'Good stuff here too'
        """
        
        employee_list = self.get_list_of_employees()
        employee_index = int(employee_number) - 1
        employee_name = employee_list[employee_index]

        tasks = []

        for task_item in Task.select().where(Task.employee == employee_name):
            tasks.append({
                "task": task_item.task, 
                "employee": task_item.employee, 
                "minutes": task_item.minutes,
                "date": task_item.date,
                "notes": task_item.notes
            })

        return tasks


    def how_to_find_previous_entries_prompt(self):
        """Prompt for how to search for previous entries

        >>> wl = Worklog()
        >>> wl.how_to_find_previous_entries_prompt()
        'How do you want to find previous entries?\\n1 = By Employee\\n2 = By Date\\n3 = By Search Term'

        """
        return "How do you want to find previous entries?\n1 = By Employee\n2 = By Date\n3 = By Search Term"

    def show_report_for_tasks(self, tasks):
        """Print out the report for a set of tasks

        >>> wl = Worklog()
        >>> wl.connect_to_database(":memory:")
        >>> wl.build_database_tables()
        True
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> tasks = wl.get_tasks_for_employee("2")
        >>> wl.show_report_for_tasks(tasks)
        Here are the tasks:
        <BLANKLINE>
        ---
        Employee: Bob
        Date: 2017-01-01
        Task: Make stuff
        Time Spent: 20 min.
        Notes: Good stuff here
        <BLANKLINE>
        >>> tasks = wl.get_tasks_for_employee("1")
        >>> wl.show_report_for_tasks(tasks)
        Here are the tasks:
        <BLANKLINE>
        ---
        Employee: Alex
        Date: 2016-10-21
        Task: Alex top task
        Time Spent: 30 min.
        Notes: Good stuff here too
        <BLANKLINE>
        ---
        Employee: Alex
        Date: 2016-10-21
        Task: Another task
        Time Spent: 30 min.
        Notes: Good stuff here too
        <BLANKLINE>
        """

        print("Here are the tasks:\n")

        for task in tasks:
            print("---")
            print("Employee: {}".format(task["employee"]))
            print("Date: {}".format(task["date"]))
            print("Task: {}".format(task["task"]))
            print("Time Spent: {} min.".format(task["minutes"]))
            print("Notes: {}".format(task["notes"]))
            print("")
    

    def validate_date(self, date):
        """Make sure the date is in the proper format

        >>> wl = Worklog()
        >>> wl.validate_date("2017-01-02")
        True
        >>> wl.validate_date("not a date")
        False

        """

        pattern = re.compile("^\d\d\d\d-\d\d-\d\d$")
        if pattern.match(date):
            return True
        else:
            return False

    def validate_date_number(self, date_number):
        """Make sure the data number is valid

        >>> wl = Worklog()
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.validate_date_number("1")
        True
        >>> wl.validate_date_number("2")
        True
        >>> wl.validate_date_number("3")
        False
        """

        pattern = re.compile("^[1-{}]$".format(len(self.get_list_of_dates())))
        if pattern.match(date_number):
            return True
        else:
            return False

    def validate_employee_number(self, employee_number):
        """Make sure the employee number is valid

        >>> wl = Worklog()
        >>> wl.add_task({"employee": "Bob", "task": "Make stuff", "minutes": 20, "notes": "Good stuff here", "date": "2017-01-01"})
        >>> wl.add_task({"employee": "Alex", "task": "Alex top task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.add_task({"employee": "Alex", "task": "Another task", "minutes": 30, "notes": "Good stuff here too", "date": "2016-10-21"})
        >>> wl.validate_employee_number("1")
        True
        >>> wl.validate_employee_number("3")
        False
        >>> wl.validate_employee_number("")
        False
        >>> wl.validate_employee_number("asdf")
        False
        """
       
        pattern = re.compile("^[1-{max}]$".format(max=len(self.get_list_of_employees())))
        if pattern.match(employee_number):
            return True
        else:
            return False


    def validate_lookup_type(self, lookup_type):
        """Makes sure that lookup_type is valid

        >>> wl = Worklog()
        >>> wl.validate_lookup_type("1")
        True
        >>> wl.validate_lookup_type("3")
        True
        >>> wl.validate_lookup_type("")
        False
        >>> wl.validate_lookup_type("4")
        False
        """

        pattern = re.compile("^[1-3]$")
        if pattern.match(lookup_type):
            return True
        else:
            return False


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

    def validate_minutes(self, minutes_as_string):
        """Make sure the string sent to minutes will
        convert to an integer properly

        >>> wl= Worklog()
        >>> wl.validate_minutes("10")
        True
        >>> wl.validate_minutes("asdf")
        False

        """
        
        pattern = re.compile("^\d+$")
        if pattern.match(minutes_as_string):
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
        wl.connect_to_database("database.db")
        wl.build_database_tables()

        keep_going = True

        while keep_going:

            wl.clear_screen()
            print("What would you like to do?") 
            wl.display_main_prompt()
            check_input = wl.ask_for_input()
            while not wl.validate_main_prompt_input(check_input):
                wl.clear_screen()
                print("That wasn't a valid option. Try again.")
                wl.display_main_prompt()
                check_input = wl.ask_for_input()

            # Add a new task selected
            if check_input == "1":

                # Get the employee name
                wl.clear_screen()
                wl.display_employee_name_prompt()
                employee = wl.ask_for_input()
                while not wl.validate_name(employee):
                    wl.clear_screen()
                    print("Names can only contain letters, spaces, and periods.")
                    print("Names also cannot be empty. Try again.")
                    employee = wl.ask_for_input()

                # Get the task name
                wl.clear_screen()
                wl.display_name_of_task_prompt()
                task = wl.ask_for_input()
                while not wl.validate_task(task):
                    wl.clear_screen()
                    print("The task can't be empty. Try again.")
                    task = wl.ask_for_input()

                # Get the time
                wl.clear_screen()
                wl.display_minutes_prompt()
                minutes_as_string = wl.ask_for_input()
                while not wl.validate_minutes(minutes_as_string):
                    wl.clear_screen()
                    print("The number of minutes for the task must be an integer. Try again.")
                    minutes_as_string = wl.ask_for_input()

                minutes = int(minutes_as_string)

                # Get optional notes
                wl.clear_screen()
                wl.display_notes_prompt()
                notes = wl.ask_for_input()

                # Add everything to the database.
                wl.add_task({"employee": employee, "task": task, "minutes": minutes, "notes": notes, "date": strftime("%Y-%m-%d", gmtime()) })
                wl.clear_screen()
                print("Task added. Press Enter/Return continue")
                input()
                

            # Lookup tasks.
            elif check_input == "2":
                wl.clear_screen()
                wl.display_lookup_prompt()
                lookup_type = wl.ask_for_input()
                while not wl.validate_lookup_type(lookup_type):
                    wl.clear_screen()
                    print("That wasn't a valid option. Try again.")
                    wl.display_lookup_prompt()
                    lookup_type = wl.ask_for_input()

                # Lookup by Employee
                if lookup_type == "1":
                    wl.clear_screen()
                    wl.display_employee_selection_prompt(wl.get_list_of_employees())
                    employee_number = wl.ask_for_input()
                    while not wl.validate_employee_number(employee_number):
                        wl.clear_screen()
                        print("That was not a valid emplyee")
                        wl.display_employee_selection_prompt(wl.get_list_of_employees())
                        employee_number = wl.ask_for_input()
                    
                    wl.clear_screen()
                    tasks = wl.get_tasks_for_employee(employee_number)
                    wl.show_report_for_tasks(tasks)
                    print("Press Enter/Return to continue.")
                    input()

                # Lookup by date 
                elif lookup_type == "2":
                    wl.clear_screen()
                    dates = wl.get_list_of_dates()
                    wl.display_date_selection_prompt(dates)
                    date_number = wl.ask_for_input()
                    while not wl.validate_date_number(date_number):
                        wl.clear_screen()
                        print("That was not a valid date. Try again.")
                        wl.display_date_selection_prompt(dates)
                        date_number = wl.ask_for_input()

                    wl.clear_screen()
                    tasks = wl.get_tasks_for_date(date_number)
                    wl.show_report_for_tasks(tasks)
                    print("Press Enter/Return to continue.")
                    input()

                # Lookup by search term 
                elif lookup_type == "3":
                    wl.clear_screen()
                    wl.display_search_prompt()

                else:
                    # This should never occur.
                    print("ERROR: Lookup type is broken.")
            
            # Quit
            else:
                print("Thanks for using the task worklog!")
                keep_going = False
                



"""
[x] - As a user of the script, I should be able to choose whether to add a new entry or lookup previous entries.
[x] - As a user of the script, if I choose to enter a new work log, I should be able to provide my name, a task name, a number of minutes spent working on it, and any additional notes I want to record.
[x] - As a user of the script, if I choose to find a previous entry, I should be presented with three options: find by employee, find by date, find by search term.
[] - As a user of the script, if finding by date, I should be presented with a list of dates with entries and be able to choose one to see entries from.
[] - As a user of the script, if finding by a search term, I should be allowed to enter a string and then be presented with entries containing that string in the task name or notes.
[x] - As a user of the script, if finding by employee, I should be allowed to enter employee name and then be presented with entries with that employee as their creator.
[] - As a fellow developer, I should find at least 50% of the code covered by tests. I would use coverage.py to validate this amount of coverage.
[] - Make sure the tool works when the database is empty.
"""

