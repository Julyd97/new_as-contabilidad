from flask_wtf import FlaskForm
from wtforms import BooleanField, validators,ValidationError, StringField, PasswordField, widgets, SelectMultipleField, IntegerField

from supplier.models import Proveedor