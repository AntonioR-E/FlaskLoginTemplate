from flask_wtf import FlaskForm, RecaptchaField
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError



from user.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
        ])

class RegisterForm(FlaskForm):
    first_name = StringField('First Name',[validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email Address', [
        validators.DataRequired(),
        validators.Email()
        ]
    )
    username = StringField('Username',[
        validators.DataRequired(),
        validators.length(min=4, max=25)
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password must match'),
        validators.length(min=8,max=30)
    ])
    confirm = PasswordField('Repeat Password')
    # recaptcha = RecaptchaField()

    def validate_username(form, field):
        if User.objects.filter(username=field.data).first():
            raise ValidationError('Username already exist')

    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email is already in use")
