"""
app/features/identity/exceptions.py

Here i will try to generat my own errors exceptions
"""


class InvalidEmailError(Exception):
    """
    Emails violates domain rules in that case i will call this
    """

    pass


class MyAppLogicError(Exception):
    """
    i wish thsi shoudl not happens but if it happens i need
    to use and check and recorrect this
    """

    pass
