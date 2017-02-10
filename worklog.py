"""Worklog with a database back end
"""

import re

class Worklog:

    def main_prompt(self):
        """Return the main prompt value
        
        >>> wl = Worklog()
        >>> wl.main_prompt()
        '1 = Add\\n2 = Lookup'
        """
        return("1 = Add\n2 = Lookup")

    def ask_for_input(self):
        """Generic method to gather user input to
        pass on to other methods for validaiton.
        """
        input("> ")

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



if __name__ == "__main__":
    import doctest
    if doctest.testmod().failed:
        print("--- Tests Failed ---")
    else:
        print("--- Tests Passed ---\n")
        wl = Worklog()
        print(wl.main_prompt())
        # wl.ask_for_input()
        wl.get_new_entry_data()


