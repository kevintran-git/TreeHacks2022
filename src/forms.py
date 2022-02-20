from flask_wtf.file import FileRequired  # , FileAllowed
from wtforms import Form, StringField, IntegerField, BooleanField, FileField
# from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired


class EventPostForm(Form):
    name = StringField('')
    amount = StringField('')
    phone = StringField('')
    source = StringField('')
    location = StringField('')
    notes = StringField('')

class DistributorPostForm(Form):
    pass