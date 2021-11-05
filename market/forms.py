from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

# Form Validation with WTForms
# DataRequired(): Checks the field’s data is ‘truthy’ otherwise stops the validation chain.
class RegisterForm(FlaskForm): #inherit FlaskForm form flask_wtf
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first() #first() will return Null if there no one -> easy for fig bug
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address ')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Acount')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')


