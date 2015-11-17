from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    """Login form"""

    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditProfileForm(Form):
    """Edit profile form"""

    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about me', validators=[Length(min=0, max=140)])
