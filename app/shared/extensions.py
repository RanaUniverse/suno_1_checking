"""
app/shared/extensions.py

This is here i will keep flask-related extra things
"""

from flask_login import LoginManager  # type: ignore
from flask_wtf import CSRFProtect  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore

login_manager = LoginManager()

csrf = CSRFProtect()

flask_bcrypt = Bcrypt()
