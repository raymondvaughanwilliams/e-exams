# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from structure import db,photos 
from structure.models import User
from structure.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from structure.users.picture_handler import add_profile_pic
import secrets
import requests

users = Blueprint('users',__name__)

# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    print("hghgj")
    # if form.validate_on_submit():
    if request.method == 'POST':
        print("df")
        user = User(email=form.email.data,
                    name=form.name.data,
                    username=form.username.data,
                    password=form.password.data,
                    last_name=form.last_name.data,role=form.role.data,
                    number=form.number.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        if form.role.data == 'user':
            return redirect(url_for('users.login'))
        else:
            return redirect(url_for('users.vendorregister',id=user.id))
            

    return render_template('register.html',form=form)



@users.route('/vendorregister/<int:id>',methods=['GET','POST'])
def vendorregister(id):
    form = RegistrationForm()
    user = User.query.filter_by(id=id).first()

    # if form.validate_on_submit():
    if request.method == 'POST':
        print("df")
        print(request.files.get('certificate'))
        if request.files.get('certificate'):
            print(form.certificate.data)
        # if form.certificate.data is not None:

            image = photos.save(request.files['certificate'], name=secrets.token_hex(10) + ".")
            image= "static/images/certificates/"+image
        else:
            image = "static/images/noimage.JPG"  
        user.business_name  = form.company.data
        user.biography = form.bio.data
        user.parts = form.parts.data
        user.cars = form.cars.data
        user.certificate = image
        user.status = "unverifieed"
        user.location  = form.location.data
        user.returnable = form.returnable.data
        user.return_period = form.returnperiod.data
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('users.login'))

            

    return render_template('web/vendorregister.html',form=form)



@users.route('/', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        
        userr = User.query.filter_by(email=form.email.data).first()
        


        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        # if user is not None and user.check_password(form.password.data) and user.role == 'admin':
        #     #Log in the user

        #     login_user(user)
        #     flash('Logged in successfully.')



        #     # If a user was trying to visit a page that requires a login
        #     # flask saves that URL as 'next'.
        #     next = request.args.get('next')

        #     # So let's now check if that next exists, otherwise we'll go to
        #     # the welcome page.
        #     if next == None or not next[0]=='/':
        #         next = url_for('userportal.userdash')

        #     return redirect(next)

        if user is not None and user.check_password(form.password.data)  :
            #Log in the user
            session['name'] = userr.name
            session['role'] = userr.role
            session['email'] = form.email.data
            session['id'] = user.id
            print("session")
            print(session['name'])
            login_user(user)
            flash('Logged in successfully.')
            if userr.role == "student":
                print("logging student in")

                return redirect(url_for('exam.exams'))
            elif userr.role == "invigilator":
                print("logging invigilator in")

                return redirect(url_for('exam.iexams'))




            # If a user was trying to visit a page that requires a login
            # # flask saves that URL as 'next'.
            # next = request.args.get('next')

            # # So let's now check if that next exists, otherwise we'll go to
            # # the welcome page.
            # if next == None or not next[0]=='/':
            #     next = url_for('exam.exams')
            

            return redirect(next)
        else:
            session['loginmsg'] = "Invalid credentials. Try again"
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('exam.exams')
            

            return redirect(next)




    return render_template('login.html', form=form)

# logout
@users.route("/logout")
def logout():
    logout_user()
    session.pop('email',None)
    session.pop('name',None)
    session.pop('role',None)
    # session.pop('loginmsg',None)

    return redirect(url_for("users.login"))


# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    userinfo = User.query.filter_by(email=session["email"]).first_or_404()

    form = UpdateUserForm()

    if request.method == 'POST':

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.number = form.number.data
        current_user.location = form.location.data
        current_user.pref_help = form.pref_help.data
        current_user.pref_therapistgender = form.pref_gender.data
        current_user.pref_medium = form.pref_medium.data
        

        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('userportal.uprofile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('userportal/profile.html', profile_image=profile_image, form=form,userinfo=userinfo)

















# user's list of Blog posts
