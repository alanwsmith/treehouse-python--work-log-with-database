Treehouse Work Log w/ Database Python Project
=============================================

This is my run at Project 4 from the Treehouse Python/Django course. 

Usage
-----

Run the script with:

    python3 worklog.py


Specs
-----

The specifications for the project are found at:

    https://teamtreehouse.com/projects/work-log-with-a-database

One spec is for:

> As a user of the script, if finding by employee, I should be allowed to enter employee name and then be presented with entries with that employee as their creator. 

I setup a list of employees to choose from instead of a free form text field. This reduces potential problems with mis-spellings. 


Issues with coverage.py
-----------------------

Running the `coverage.py` command `coverage run worklog.py` on my system reports several errors like:

    **********************************************************************
    File "worklog.py", line 267, in __main__.Worklog.get_list_of_employees
    Failed example:
        employee_list[0]
    Expected:
        'Alex'
    Got:
        u'Alex'

In every case the `u` shows up in front of the string. These issues only show up when running `coverage`. The script is setup to run the test suite before each execution and they all pass there. 

I'd keep digging until I solved the issue if this was an app destined for production. For now, I'm leaving it since it's a higher priority to continue to make progress in the course and even with the issue `coverage.py` reports 58% test coverage which crosses the > 50% threshold for acceptance. 

While I don't like leaving that type of bug, the limited time available for the exercises necessitates moving on.


PEP8
----

There are a couple PEP8 violations of line length. These are based on the 
way the test suite looks for returned values. Probably fixable, but the 
higher priority is making progress in the course.

