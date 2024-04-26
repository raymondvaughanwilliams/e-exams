from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField,TimeField
from flask_wtf import FlaskForm, Form
from wtforms.fields.html5 import DateField,DateTimeField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo ,Length
from wtforms import ValidationError
from wtforms_components import TimeField



class BookingForm(FlaskForm):
    name = StringField('Contact Name', validators=[DataRequired(),Email()])
    # company = StringField('Company Name', [validators.Length(min=4, max=25)])
    date = DateField('Choose Date', [validators.DataRequired()] ,format='%Y-%m-%d')
    phone = StringField('Mobile', [validators.Length(min=6, max=35)])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    message = TextAreaField('Message', [validators.Length(min=4, max=140)]) 
    location = StringField('Location',[validators.Length(min=4,max=140)])
    time= TimeField('Time', [validators.DataRequired()])
    submit = SubmitField('BOOK THERAPIST')


class UpdateSessionForm(FlaskForm):
    date = DateField('Choose Date', [validators.DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',[validators.DataRequired()])
    submit = SubmitField('Reschedule')



class ResultForm(FlaskForm):
    name = StringField('Text', [validators.DataRequired()])
    subject = StringField('Text')
    result = IntegerField('Result')
    index_number = StringField('Index Number')

    # subject= SelectField('Subject')
    year = SelectField('Year', choices=[(str(year), str(year)) for year in range(2023, 2034)])
    submit = SubmitField('Add')

class StudentForm(FlaskForm):
    name = StringField('Text', [validators.DataRequired()])
    subject = StringField('Text')
    index_number = StringField('Index Number')
    year = SelectField('Year', choices=[(str(year), str(year)) for year in range(2023, 2034)])
    submit = SubmitField('Add')

class CheckResultForm(FlaskForm):
    
    index_number = StringField('Index Number')
    year = SelectField('Year', choices=[(str(year), str(year)) for year in range(2023, 2034)])
    submit = SubmitField('CHECK')

class CheckerForm(FlaskForm):
    result = IntegerField('Result')
    # subject= SelectField('Subject')
    submit = SubmitField('Add')
    

class Addtherapist(Form):
    title = StringField('Title', [validators.DataRequired()])
    
    
class NewsletterForm(Form):
    name = StringField('Name')
    phone = StringField('Phone')
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Join Newsletter')
    
    

    
class DeliveryForm(FlaskForm):
    # destination = SelectField("Destination", validators=[DataRequired()], choices=[(destination.id, destination.name) for destination in destinations])
    # location = SelectField("Location", validators=[DataRequired()], choices=[(destination.id, destination.name) for destination in destinations])
    status = SelectField("Status", validators=[DataRequired()], choices=[("undelivered","Not Delivered"),('delivered','Delivered')])
    start_date = DateField('Choose Start Date', [validators.DataRequired()] )
    end_date = DateField('Choose End Date', [validators.DataRequired()])
    arrival_date = DateField('Arrival Date', [validators.DataRequired()])
    item_name = StringField("Item Name", validators=[Length(min=3, max=120)])
    item_description = StringField("Item Description", validators=[DataRequired(), Length(min=3, max=120)])
    item_weight = FloatField("Item Weight")
    item_dimension = StringField("Item Dimension", validators=[Length(min=3, max=120)])
    note =  TextAreaField('Note', [validators.Length(min=4, max=140)]) 
    traveller_note =  TextAreaField('Note', [validators.Length(min=4, max=140)]) 
    amount = FloatField("Amount", validators=[DataRequired()])
    ticket = FileField('Ticket', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])

    submit = SubmitField('Submit')

    
    
    
class FilterForm(FlaskForm):
    # destination = SelectField("Destination", choices=[(destination.id, destination.name) for destination in destinations])
    # location = SelectField("Location", choices=[(destination.id, destination.name) for destination in destinations])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    number = StringField('Premium Amount')
    premium_amount = StringField('Premium Amount')
    location = StringField('Location')
    language = StringField('Language')
    country = StringField('Country')
    society = StringField('Society')
    cooperative = StringField('Cooperative')
    ordernumber = StringField('Order Number')
    submit = SubmitField('Submit') 
    
    
class ContactForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    hidden = HiddenField('Hidden',default="contact" )
    submit = SubmitField('Submit')
   
   
class FarmerForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    number = StringField('Premium Amount')
    farmercode = StringField('Farmer Code')
    premium_amount = StringField('Premium Amount')
    location = StringField('Location')
    language = StringField('Language')
    country = StringField('Country')
    cooperative = StringField('Cooperative')
    ordernumber = StringField('Order Number')
    society = StringField('Society')
    cashcode = StringField('Cashcode')
    index_number = StringField('Index Number')
    uploadfile = FileField('Upload', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Submit') 
    
    
class RequestForm(Form):
    name = StringField('Name',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    model_year = StringField('Model Year', validators=[DataRequired()])
    car_make = StringField('Car Type', validators=[DataRequired()])
    car_model = StringField('Model ', validators=[DataRequired()])
    quantity = StringField('Quantity ', validators=[DataRequired()])
    note =  TextAreaField('Note', [validators.Length(min=4, max=140)]) 

    submit = SubmitField('Submit')
    
    
class BidForm(Form):
    price = IntegerField('Price',validators=[DataRequired()])
    quantity = StringField('Quantiy', validators=[DataRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Submit')
    
    
class AcceptBidForm(Form):
    status= SelectField('Status', validators=[DataRequired()],choices=[('accepted', 'accept'),('deny','deny')])
    deliverystatus= SelectField("Status", validators=[DataRequired()], choices=[("undelivered","Not Delivered"),('delivered','Delivered')])
    delivery= SelectField('Choose Purchase Method', validators=[DataRequired()],choices=[('needpartsdelivery', 'Use Need Parts Secure Delivery'),('standard','Speak to Vendor')])
    note =  TextAreaField('Note', [validators.Length(min=4, max=140)]) 
    submit = SubmitField('Submit')
    
    
class ReviewForm(Form):
    text = TextAreaField('Text', validators=[DataRequired()])
    hidden = HiddenField('Hidden', validators=[DataRequired()])
    submit = SubmitField('Submit')