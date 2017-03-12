from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(Form):
    url = StringField('Enter URL to download and tag it',
                      validators=[Required()])
    submit = SubmitField('Tag!')


class CheckForm(Form):
    check = SubmitField('Check')
