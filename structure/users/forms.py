from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField ,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from structure.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('UserName',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    last_name = StringField('Last Name')
    number = StringField('Number',validators=[DataRequired()])
    role = SelectField('Sign Up as a:',validators=[DataRequired()],choices=[('student', 'student'), ('invigilator','invigilator'),('examiner','examiner')])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    bio = StringField('Bio')
    company = StringField('Company Name')
    parts = TextAreaField('Parts you sell')
    cars  = TextAreaField('Names of cars whose parts you deal in')
    certificate = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    location = StringField('Location')
    returnable = SelectField('Returnable',validators=[DataRequired()],choices=[('yes', 'Yes'), ('no', 'No')])
    returnperiod = SelectField('Return Period for all parts(Warranty)',validators=[DataRequired()],choices=[('one', 'One day'), ('two', 'Two days'), ('three', 'Three days'), ('five', 'Five days'),('seven','One Week'),('fourteen','Two weeeks'),('thirty','One Month'),('ninety','3 months')])
    
    submit = SubmitField('Sign Up!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    plan = StringField('Plan', validators=[DataRequired()])
    number = StringField('Number', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    location = StringField('Location', validators=[DataRequired()])
    pref_help = StringField('What are you seeking help for?')
    pref_medium = StringField('What is your preferred medium for the session? eg whatsapp, zoom etc')
    pref_gender = StringField('Do you have a preferred gender for the session?')
    submit = SubmitField('Update Details!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')




class UpdateAgentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    plan = StringField('Plan', validators=[DataRequired()])
    number = StringField('Number', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    location = StringField('Location', validators=[DataRequired()])
    pref_help = StringField('What are you seeking help for?')
    pref_medium = StringField('What is your preferred medium for the session? eg whatsapp, zoom etc')
    pref_gender = StringField('Do you have a preferred gender for the session?')
    specialty = StringField('What is your specialty?')
    biography = TextAreaField('Biography')
    experience = StringField('Years of experience.')
    baseprice = IntegerField('Base Price')
    platform = StringField('What platforms can you have have your sessions? Eg zoom, In Person')
    submit = SubmitField('Update Details!')

    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')