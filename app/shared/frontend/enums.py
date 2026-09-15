"""
app/shared/frontend/enums.py

Here i will keep the enums to easily use in differnet cases
"""

from enum import StrEnum


class FlashCategory(StrEnum):
    """
    These are the values coming form the Bootstrap5 colors
    I will use this values there to shows or distinguishes easily
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"
