from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = TextField('login name ', validator = [Required()])
#    password = PasswordField('password', validator = [Required()])
    submit = SubmitField('Submit')
