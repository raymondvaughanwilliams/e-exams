#models.py
from unicodedata import name
from structure import db,login_manager,app,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager
from datetime import datetime

# class UserTherapySession(db.Model):
#     __tablename__ = 'usertherapysessions'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship("User", foreign_keys=user_id)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))


class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    name = db.Column(db.String(64),nullable=True)
    last_name = db.Column(db.String(64),nullable=True)
    password_hash = db.Column(db.String(128))
    number = db.Column(db.String(128))
    location = db.Column(db.String(128))
    role = db.Column(db.String,nullable=True)
    phone_number = db.Column(db.String)
    # biography = db.Column(db.String)
    status=db.Column(db.String,default="unverified")
    index_number = db.Column(db.String)
    completed_year=db.Column(db.String)
    # rec_payment_id = db.Column(db.Integer,db.ForeignKey('payments.id'),nullable=True)
    # payments = db.relationship('Payment',backref='users',lazy=True)


    # roles = db.relationship('Roles', secondary='user_roles')


    def __init__(self,email,username,password,name,role,last_name,number):
        self.email = email
        self.username = username
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.role = role
        # self.rem_chatweeks = rem_chatweeks
        # self.rem_sessions=rem_sessions
        # self.pref_medium = pref_medium
        # self.pref_help = pref_help
        # self.pref_therapistgender = pref_therapistgender
        self.last_name = last_name
        self.number = number

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"




# # class WebFeature(db.Model):
# #     __tablename__ = "webfeatures"


# #     id = db.Column(db.Integer,primary_key=True)
# #     date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
# #     title = db.Column(db.String(140),nullable=False)
# #     wtext = db.Column(db.Text,nullable=False)
# #     price = db.Column(db.Float,nullable=True)
# #     type = db.Column(db.String(100),nullable=True)
# #     email = db.Column(db.String(40),nullable=True)
# #     city = db.Column(db.String(50),nullable=True)
# #     phone = db.Column(db.String(50),nullable=True)



# #     def __init__(self,title,wtext,date):
# #         self.title = title
# #         self.wtext = wtext
# #         self.date = date
     

# #     def __repr__(self):
# #         return f"Post ID: --- {self.title}---{self.wtext}--{self.date}"




# # class Therapist(db.Model):
# #     __tablename__ = 'therapists'

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String)
# #     specialty = db.Column(db.String)
# #     location = db.Column(db.String)
# #     email = db.Column(db.String)
# #     phone_number = db.Column(db.String)
# #     biography = db.Column(db.String)
# #     qualifications = db.Column(db.String)
# #     years_of_experience = db.Column(db.Integer)
# #     license_number = db.Column(db.String)
# #     insurance_provider = db.Column(db.String)



# # class TherapistDetails(db.Model):
# #     __tablename__ = 'therapistdetails'

# #     id = db.Column(db.Integer, primary_key=True)
# #     specialty = db.Column(db.String)
# #     location = db.Column(db.String)
# #     email = db.Column(db.String)
# #     phone_number = db.Column(db.String)
# #     biography = db.Column(db.String)
# #     qualifications = db.Column(db.String)
# #     years_of_experience = db.Column(db.Integer)
# #     license_number = db.Column(db.String)
# #     insurance_provider = db.Column(db.String)
# #     platforms = db.Column(db.String)
# #     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
# #     user= db.relationship('User',backref='users',lazy=True)
    
    



# class About(db.Model):


#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(140),nullable=False)
#     subtitle= db.Column(db.String(140),nullable=True)
#     atext = db.Column(db.Text,nullable=False)
#     image = db.Column(db.String(64),nullable=True,default='default_profile.png')
#     about_image = db.Column(db.String(64),nullable=True,default='default_profile.png')
#     location = db.Column(db.String(140),nullable=False,default='location')
#     number = db.Column(db.Integer,nullable=True)
#     email = db.Column(db.String(64),unique=True,index=True)
#     contact_subtitle = db.Column(db.String(140),nullable=True)
#     about_subtitle = db.Column(db.String(140),nullable=True)
#     feature_subtitle = db.Column(db.String(140),nullable=True)
#     feature_paragraph = db.Column(db.Text,nullable=True)
#     faq_title = db.Column(db.String(140),nullable=True)
#     faq_subtitle = db.Column(db.String(140),nullable=True)
#     faq_paragraph = db.Column(db.String(140),nullable=True)
#     testimonial_title = db.Column(db.String(140),nullable=True)
#     testimonial_subtitle = db.Column(db.String(140),nullable=True)
#     testimonial_paragraph = db.Column(db.String(140),nullable=True)
#     team_title = db.Column(db.String(140),nullable=True)
#     team_subtitle = db.Column(db.String(140),nullable=True)
#     team_paragraph = db.Column(db.String(140),nullable=True)
#     logo = db.Column(db.String(64),nullable=True,default='default_profile.png')
#     carousel_image_1 = db.Column(db.String(64),nullable=True,default='default_profile.png')

#     def __init__(self,title,text,user_id,location,number,email,contact_subtitle,about_subtitle,
#     feature_subtitle,feature_paragraph,faq_title,faq_subtitle,faq_paragraph,testimonial_title,
#     testimonial_subtitle,testimonial_paragraph,team_title,team_subtitle,team_paragraph,logo,carousel_image_1,subtitle,about_image):
#         self.title = title
#         self.text = text
#         self.location = location
#         self.number = number
#         self.email = email
#         self.contact_subtitle = contact_subtitle
#         self.about_subtitle = about_subtitle
#         self.feature_subtitle = feature_subtitle
#         self.feature_paragraph = feature_paragraph
#         self.faq_title = faq_title
#         self.faq_subtitle = faq_subtitle
#         self.faq_paragraph = faq_paragraph
#         self.testimonial_title = testimonial_title
#         self.testimonial_subtitle = testimonial_subtitle
#         self.testimonial_paragraph = testimonial_paragraph
#         self.team_title = team_title
#         self.team_subtitle = team_subtitle
#         self.team_paragraph = team_paragraph
#         self.logo = logo
#         self.subtitle = subtitle
#         self.about_image = about_image
#         self.carousel_image_1 = carousel_image_1

#     def __repr__(self):
#         return f"Post ID: {self.id} -- {self.title} -- {self.location} -- {self.number} -- {self.email} -- {self.contact_subtitle}-- {self.about_subtitle}-- {self.feature_subtitle}-- {self.feature_paragraph}-- {self.faq_title}-- {self.faq_subtitle}-- {self.faq_paragraph}-- {self.testimonial_title}-- {self.testimonial_subtitle}-- {self.testimonial_paragraph}-- {self.team_title}-- {self.team_subtitle}-- {self.team_paragraph} -- {self.logo} -- {self.carousel_image_1}"



# # class Price(db.Model):
# #     __tablename__ = "prices"


# #     id = db.Column(db.Integer,primary_key=True)
# #     title = db.Column(db.String(140),nullable=False)
# #     amount = db.Column(db.Text,nullable=False)
# #     features = db.Column(db.Text(64),nullable=False,default='default_profile.png')
# #     numsessions = db.Column(db.Integer,nullable=True)
# #     numchatweeks = db.Column(db.Integer,nullable=True)

# #     def __init__(self,title,amount,features,numsessions,numchatweeks):
# #         self.title = title
# #         self.amount = amount
# #         self.features = features 
# #         self.numsessions = numsessions
# #         self.numchatweeks = numchatweeks

# #     def __repr__(self):
# #         return f"Post ID: {self.id} -- {self.title}"




# class Faq(db.Model):


#     id = db.Column(db.Integer,primary_key=True)
#     question = db.Column(db.String(140),nullable=False)
#     answer = db.Column(db.Text,nullable=False)

#     def __init__(self,question,answer):
#         self.question = question
#         self.answer = answer

#     def __repr__(self):
#         return f"{self.question} -- {self.answer}"




# class Testimonial(db.Model):


#     id = db.Column(db.Integer,primary_key=True)
#     company = db.Column(db.String,nullable=True)
#     name = db.Column(db.String,nullable=True)
#     text = db.Column(db.String(140),nullable=True)
#     rating = db.Column(db.Integer,nullable=True)


#     def __init__(self,name,company,text,rating):
#         self.name = name
#         self.company = company
#         self.text = text
#         self.rating = rating

#     def __repr__(self):
#         return f"Post ID: {self.id} -- {self.name} -- {self.company} -- {self.text} -- {self.rating}"


# class StudentResult(db.Model):
#     __tablename__ = "student_results"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     subject = db.Column(db.String(128), nullable=False)
#     year = db.Column(db.String(128))
#     result = db.Column(db.Integer, nullable=False)
#     index_number = db.Column(db.String(128))
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     student = db.relationship("User", foreign_keys=[student_id])
#     subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
#     subject = db.relationship("Subject", foreign_keys=[subject_id])

#     def __repr__(self):
#         return f'<StudentResult {self.name}>'


# class Subject(db.Model):
#     __tablename__ = "subjects"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)


#     def __repr__(self):
#         return f'<StudentResult {self.name}>'



# class PartRequest(db.Model):
#     __tablename__ = "partrequests"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     description = db.Column(db.String(512), nullable=False)
#     model_year = db.Column(db.Integer, nullable=False)
#     car_make = db.Column(db.String(128), nullable=False)
#     car_model = db.Column(db.String(128), nullable=False)
#     note = db.Column(db.String(128), nullable=True)
#     quantity = db.Column(db.Integer, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship("User", foreign_keys=[user_id])
#     status = db.Column(db.String(16), nullable=False)


#     def __repr__(self):
#         return f'<Part {self.name}>'

# class Bid(db.Model):
#     __tablename__ = 'bids'
#     id = db.Column(db.Integer, primary_key=True)
#     part_id = db.Column(db.Integer, db.ForeignKey('partrequests.id'), nullable=False)
#     parts = db.relationship("PartRequest", foreign_keys=[part_id])
#     vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     vendors  = db.relationship("User", foreign_keys=[vendor_id])
#     price = db.Column(db.Float, nullable=False)
#     quantity = db.Column(db.Integer, nullable=True)
#     status = db.Column(db.String(16), nullable=False)
#     delivery = db.Column(db.String(16), nullable=True)
#     note = db.Column(db.String(255), nullable=True)

#     def __repr__(self):
#         return f'<Bid {self.id}>'


# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship("User", foreign_keys=[user_id])
#     text = db.Column(db.String(255), nullable=True)
#     date = db.Column(db.Date)
#     vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
#     vendors  = db.relationship("User", foreign_keys=[vendor_id])
    


# class Farmer(db.Model):
#     __tablename__ = "farmers"
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255))
#     last_name = db.Column(db.String(255))
#     number = db.Column(db.Integer())
#     premium_amount = db.Column(db.Integer())
#     location = db.Column(db.String(255))
#     country = db.Column(db.String(255))
#     cashcode = db.Column(db.String(255))
#     date_added = db.Column(db.Date,default=datetime.now)
#     last_modified = db.Column(db.Date,default=datetime.now)
#     language = db.Column(db.String(255))
#     society = db.Column(db.String(255))
#     farmercode = db.Column(db.String(255))
#     cooperative = db.Column(db.String(255))
#     ordernumber = db.Column(db.String(255))
    
    
# class EcomRequest(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     date = db.Column(db.DateTime,default=datetime.utcnow)
#     number = db.Column(db.Integer())
#     cashcode = db.Column(db.String())
#     farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=True)
#     farmers  = db.relationship("Farmer", foreign_keys=[farmer_id])
#     country = db.Column(db.String(255), nullable=True)
#     disposition = db.Column(db.String())
#     sms_disposition = db.Column(db.String())
#     sms_attempts = db.Column(db.Integer(),default =0)
  
   
    
 


class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    jitsi_room_id = db.Column(db.String(100))
    # status = db.Column(db.String(100), default='active')

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_text = db.Column(db.Text)
    answers = db.relationship('Answer', backref='questions', lazy=True)

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer_text = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship("Exam", foreign_keys=[exam_id])
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship("Question", foreign_keys=[question_id])
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))
    answer = db.relationship("Answer", foreign_keys=[answer_id])



class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # image_path = db.String(200)
    image_location = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship("Exam", foreign_keys=[exam_id])

class Images(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    image_path = db.String(200)
    image_location = db.String(200)
    img_src = db.String(200)
    # srccc
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship("Exam", foreign_keys=[exam_id])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
