"""Worklog with a database back end
"""

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


if __name__ == "__main__":
    import doctest
    if doctest.testmod().failed:
        print("--- Tests Failed ---")
    else:
        print("--- Tests Passed ---\n")
        wl = Worklog()
        print(wl.main_prompt())
        wl.ask_for_input()

