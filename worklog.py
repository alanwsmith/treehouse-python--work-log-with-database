"""Worklog with a database back end
"""

class Worklog:

    def main_prompt(self):
        """Return the main prompt value
        
        >>> wl = Worklog()
        >>> wl.main_prompt()
        1 = Add
        2 = Lookup
        """
        print("1 = Add\n2 = Lookup")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    if doctest.testmod().failed:
        print("--- Tests Failed ---")
    else:
        print("--- Tests Passed ---\n")
        wl = Worklog()
        wl.main_prompt()

