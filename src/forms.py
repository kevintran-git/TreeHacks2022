from flask_wtf.file import FileRequired  # , FileAllowed
from wtforms import Form, StringField, IntegerField, BooleanField, FileField
# from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired


class PostForm(Form):
    title = StringField('')
    org_name = StringField('')
    food_name = StringField('')
    address = StringField('')
    date = StringField('')
    allergens = StringField('')

class AcceptForm(Form):
    id = IntegerField('')

class PublishForm(Form):
    id = IntegerField('')