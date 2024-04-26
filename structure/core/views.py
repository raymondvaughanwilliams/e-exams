import atexit
import csv
import os
from os import environ
from uuid import uuid4

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, Blueprint, session, redirect, url_for, jsonify, current_app, request
from flask_login import login_required
from sqlalchemy import and_, or_, desc

from structure import db
from structure.core.forms import FilterForm, FarmerForm ,ResultForm,CheckResultForm,StudentForm
from structure.models import User, About, Farmer, EcomRequest , StudentResult , Subject

core = Blueprint('core', __name__)

API_KEY = os.environ.get('API_KEY')


def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid API key', 'status': False}), 401

    return decorated_function


@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('base.html', about=about)


@core.route('/indexd')
def indexd():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('index.html', about=about)


@core.route('/agent/dashboard')
@login_required
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    name = "ecom"
    session.pop('msg', None)

    subjects = Subject.query.order_by(desc(Subject.id)).all()
    studentresults = StudentResult.query.order_by(desc(StudentResult.id)).all()
    farmers = Farmer.query.order_by(desc(Farmer.id)).all()
    ecom_requests = EcomRequest.query.order_by(desc(EcomRequest.id)).all()

    form = FilterForm()
    if session['role'] == 'agent':
        name = user.name

    return render_template(
        'agentportal/dashboard.html',
        form=form, user=user, about=about,
        name=name, farmers=farmers, ecomrequests=ecom_requests,
        subjects=subjects,studentresults=studentresults
    )


@core.route('/claims', methods=['GET', 'POST'])
@login_required
def claims():
    ecomrequests = EcomRequest.query.all()

    form = FilterForm()

    if request.method == "POST":
        # Get the filter values from the form
        first_name = form.first_name.data
        last_name = form.last_name.data

        location = form.location.data
        number = form.number.data
        cooperative = form.cooperative.data
        country = form.country.data
        society = form.society.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            first_name_conditions = [
                EcomRequest.farmers.first_name.like(f"%{first_name}%"),
                EcomRequest.farmers.first_name.like(f"{first_name}%"),
                EcomRequest.farmers.first_name.like(f"%{first_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*first_name_conditions))
        if last_name:
            last_name_conditions = [
                EcomRequest.farmers.last_name.like(f"%{last_name}%"),
                EcomRequest.farmers.last_name.like(f"{last_name}%"),
                EcomRequest.farmers.last_name.like(f"%{last_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*last_name_conditions))
        if number:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            number_conditions = [
                EcomRequest.number.like(f"%{number}%"),
                EcomRequest.number.like(f"{number}%"),
                EcomRequest.number.like(f"%{number}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*number_conditions))
        if location:
            # Build a list of conditions that match the destination field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                EcomRequest.location.like(f"%{location}%"),
                EcomRequest.location.like(f"{location}%"),
                EcomRequest.location.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*location_conditions))
        if cooperative:
            cooperative_conditions = [
                EcomRequest.cooperative.like(f"%{cooperative}%"),
                EcomRequest.cooperative.like(f"{cooperative}%"),
                EcomRequest.cooperative.like(f"%{cooperative}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*cooperative_conditions))
        if society:
            society_conditions = [
                EcomRequest.society.like(f"%{society}%"),
                EcomRequest.society.like(f"{society}%"),
                EcomRequest.society.like(f"%{society}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*society_conditions))
        if country:
            country_conditions = [
                EcomRequest.country.like(f"%{country}%"),
                EcomRequest.country.like(f"{country}%"),
                EcomRequest.country.like(f"%{country}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*country_conditions))

        ecomrequests = EcomRequest.query.filter(and_(*conditions)).all()

    return render_template('agentportal/claims.html', form=form, ecomrequests=ecomrequests, filterform=form)


@core.route("/addfarmer", methods=["GET", "POST"])
@login_required
def addfarmer():
    form = FarmerForm()
    items = Farmer.query.all()
    if request.method == "POST":
        check_farmer = Farmer.query.filter_by(number=form.number.data).first()
        if check_farmer:
            session['msg'] = "Farmer already exists"
            return redirect(url_for("core.addfarmer"))
        else:
            farmer = Farmer(
                first_name="NA",
                last_name=form.last_name.data,
                number=form.number.data,
                premium_amount=form.premium_amount.data,
                location="NA",
                language=form.language.data,
                country=form.country.data,
                cooperative=form.cooperative.data,
                ordernumber="NA",
                cashcode=form.cashcode.data,
                farmercode=form.farmercode.data,
                society=form.society.data
            )
            db.session.add(farmer)
            db.session.commit()
            return redirect(url_for("core.farmers"))

    return render_template("agentportal/addfarmer.html", form=form, items=items)



@core.route("/addresult", methods=["GET", "POST"])
@login_required
def addresult():
    
    form = ResultForm()
    items = StudentResult.query.all()
    subjects = Subject.query.all()
    if request.method == "POST":
        print("ssmna")
        print(form.subject.data)
       
        result = StudentResult(
            name=form.name.data,
            subject=form.subject.data,
            result=form.result.data,
            index_number = form.index_number.data,
            completed_year = form.year.data
            
        )
        db.session.add(result)
        db.session.commit()
        return redirect(url_for("core.results"))

    return render_template("agentportal/addresult.html", form=form, items=items , subjects = subjects)





@core.route("/addstudent", methods=["GET", "POST"])
@login_required
def addstudent():
    
    form = ResultForm()
    items = StudentResult.query.all()
    subjects = Subject.query.all()
    if request.method == "POST":
        print("ssmna")
        print(form.subject.data)
       
        result = StudentResult(
            name=form.name.data,
            subject=form.subject.data,
            result=form.result.data,
            index_number = form.index_number.data,
            completed_year = form.year.data
            
        )
        db.session.add(result)
        db.session.commit()
        return redirect(url_for("core.results"))

    return render_template("agentportal/addresult.html", form=form, items=items , subjects = subjects)



@core.route("/results", methods=["GET", "POST"])
@login_required
def results():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    results = StudentResult.query.paginate(page, 20, False)

    session.pop('msg', None)
    session.pop('duplicates', None)

    search = "no"
    if request.method == "POST":
        search = "yes"
        # Get the filter values from the form
        name = form.name.data
        subject = form.subject.data
        result = form.result.data
        #
        # Build the SQLAlchemy filter conditions
        conditions = []
        if name:
            name_conditions = [
                StudentResult.name.like(f"%{name}%"),
                StudentResult.name.like(f"{name}%"),
                StudentResult.name.like(f"%{name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*name_conditions))
        if subject:
            subject_conditions = [
                StudentResult.subject.like(f"%{subject}%"),
                StudentResult.subject.like(f"{subject}%"),
                StudentResult.subject.like(f"%{subject}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*subject_conditions))
        if result:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            result_conditions = [
                StudentResult.result.like(f"%{result}%"),
                StudentResult.result.like(f"{result}%"),
                StudentResult.result.like(f"%{result}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*result_conditions))
       

        results = StudentResult.query.filter(and_(*conditions)).all()

    return render_template(
        "agentportal/results.html",
        results=farmers, form=form,
        filterform=form, page=page,
        search=search
    )



@core.route("/students", methods=["GET", "POST"])
@login_required
def students():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    students = User.query.filter_by(role='student').all()
#

    
    return render_template(
        "agentportal/students.html",
        students=students,
        filterform=form, page=page,
        
    )



@core.route("/farmers", methods=["GET", "POST"])
@login_required
def farmers():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    farmers = Farmer.query.paginate(page, 20, False)

    session.pop('msg', None)
    session.pop('duplicates', None)

    search = "no"
    if request.method == "POST":
        search = "yes"
        # Get the filter values from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        location = form.location.data
        number = form.number.data
        cooperative = form.cooperative.data
        country = form.country.data
        society = form.society.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            first_name_conditions = [
                Farmer.first_name.like(f"%{first_name}%"),
                Farmer.first_name.like(f"{first_name}%"),
                Farmer.first_name.like(f"%{first_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*first_name_conditions))
        if last_name:
            last_name_conditions = [
                Farmer.last_name.like(f"%{last_name}%"),
                Farmer.last_name.like(f"{last_name}%"),
                Farmer.last_name.like(f"%{last_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*last_name_conditions))
        if number:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            number_conditions = [
                Farmer.number.like(f"%{number}%"),
                Farmer.number.like(f"{number}%"),
                Farmer.number.like(f"%{number}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*number_conditions))
        if location:
            # Build a list of conditions that match the destination field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                Farmer.location.like(f"%{location}%"),
                Farmer.location.like(f"{location}%"),
                Farmer.location.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*location_conditions))
        if cooperative:
            cooperative_conditions = [
                Farmer.cooperative.like(f"%{cooperative}%"),
                Farmer.cooperative.like(f"{cooperative}%"),
                Farmer.cooperative.like(f"%{cooperative}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*cooperative_conditions))
        if society:
            society_conditions = [
                Farmer.society.like(f"%{society}%"),
                Farmer.society.like(f"{society}%"),
                Farmer.society.like(f"%{society}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*society_conditions))
        if country:
            country_conditions = [
                Farmer.country.like(f"%{country}%"),
                Farmer.country.like(f"{country}%"),
                Farmer.country.like(f"%{country}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*country_conditions))

        farmers = Farmer.query.filter(and_(*conditions)).all()

    return render_template(
        "agentportal/farmers.html",
        farmers=farmers, form=form,
        filterform=form, page=page,
        search=search
    )


@core.route("/farmer/<int:id>", methods=["POST", 'GET'])
@login_required
def farmer(id):
    form = FarmerForm()
    farmer = Farmer.query.filter_by(id=id).first()

    if request.method == "POST":
        farmer.first_name = form.first_name.data
        farmer.last_name = form.last_name.data
        farmer.number = form.number.data
        farmer.premium_amount = form.premium_amount.data
        farmer.country = form.country.data
        farmer.language = form.language.data
        farmer.society = form.society.data
        farmer.cooperative = form.cooperative.data
        farmer.cashcode = form.cashcode.data
        farmer.farmercode = form.farmercode.data

        db.session.commit()

        return redirect(url_for("core.farmers"))

    elif request.method == 'GET':
        form.first_name.data = farmer.first_name
        form.last_name.data = farmer.last_name
        form.number.data = farmer.number
        form.premium_amount.data = farmer.premium_amount
        form.language.data = farmer.language
        form.society.data = farmer.society
        form.country.data = farmer.country
        form.cooperative.data = farmer.cooperative
        form.cashcode.data = farmer.cashcode
        form.farmercode.data = farmer.farmercode.data

    return render_template("agentportal/farmer.html", farmer=farmer, form=form)




@core.route("/result/<int:id>", methods=["POST", 'GET'])
@login_required
def result(id):
    form = ResultForm()
    result = StudentResult.query.filter_by(id=id).first()

    if request.method == "POST":
        result.index_number = form.index_number.data
        # result.subject = form.subject.data
        result.result = form.result.data
   

        db.session.commit()

        return redirect(url_for("core.results"))

    elif request.method == 'GET':
        form.name.data = result.name
        form.subject.data = result.subject
        form.result.data = result.result
      

    return render_template("agentportal/result.html", result=result, form=form)



@core.route("/student/<int:id>", methods=["POST", 'GET'])
@login_required
def student(id):
    form = StudentForm()
    student = User.query.filter_by(id=id).first()

    if request.method == "POST":
        student.name = form.name.data
        student.index_number = form.index_number.data
   

        db.session.commit()

        return redirect(url_for("core.students"))

    elif request.method == 'GET':
        form.name.data = student.name
        form.index_number.data = student.index_number
      

    return render_template("agentportal/student.html", student=student, form=form)


@core.route("/delete_farmer/<int:farmer_id>", methods=['POST', 'GET'])
@login_required
def delete_farmer(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    db.session.delete(farmer)
    db.session.commit()
    return redirect(url_for('core.farmers'))

@core.route("/delete_result/<int:result_id>", methods=['POST', 'GET'])
@login_required
def delete_result(result_id):
    result = StudentResult.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('core.results'))


@core.route("/api/delete_farmers", methods=['POST', 'GET'])
def delete_farmers():
    farmers = request.args.get('farmers')
    farmers_list = [int(farmer) for farmer in farmers.split(",")]
    successfully_deleted = []
    failed = []

    for thefarmer in farmers_list:
        farmer = Farmer.query.filter_by(id=thefarmer).first()
        if farmer:
            db.session.delete(farmer)
            db.session.commit()
            successfully_deleted.append(thefarmer)
        else:
            failed.append(thefarmer)

    payload = {
        "status": True,
        "message": " Farmers deleted",
        "successful": successfully_deleted,
        "failed": failed
    }

    return jsonify(payload), 200


@core.route('/api/addfarmer', methods=['GET', 'POST'])
# @jwt_required()
def addplan():
    farmer = Farmer.query.all()

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    premium_amount = request.json['premium_amount']
    location = request.json['location']
    number = request.json['number']

    plan = Farmer(
        first_name=first_name,
        premium_amount=premium_amount,
        last_name=last_name,
        number=number,
        location=location
    )

    db.session.add(farmer)
    db.session.commit()
    status = 1
    if status == 1:
        return jsonify(first_name, last_name, premium_amount, "success")
    else:
        return jsonify("Failed")




# @core.route("/farmersapi", methods=["GET", "POST"])
# def farmersapi():
#     farmers = Farmer.query.all()
#     farmer_list = []

#     if farmers:
#         for farmer in farmers:
#             payload = {
#                 "id": farmer.id,
#                 "farmercode": farmer.farmercode,
#                 "farmerName": farmer.last_name,
#                 "premiumAmount": farmer.premium_amount,
#                 "cooperative": farmer.cooperative,
#                 "cashcode": farmer.cashcode,
#                 "society": farmer.society,
#                 "country": farmer.country,
#                 "language": farmer.language,
#                 "number": farmer.number
#             }
#             farmer_list.append(payload)

#         context = {
#             "status": True,
#             "message": " Farmer found!",
#             "data": farmer_list,
#         }

#         return jsonify(context), 200
#     else:
#         context = {
#             "status": False,
#             "message": "Farmer not found",
#             "error": "null"
#         }

#         return jsonify(context), 404

@core.route("/studentsapi", methods=["GET", "POST"])
def studentsapi():
    students = User.query.filter_by(role='student').all()
    student_list = []

    if students:
        for student in students:
            payload = {
                "id": student.id,
                "name": student.name,
                "index_number": student.index_number,
                "completed_year": student.completed_year,
             
            }
            student_list.append(payload)

        context = {
            "status": True,
            "message": " student found!",
            "data": student_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "student not found",
            "error": "null"
        }

        return jsonify(context), 404

@core.route("/resultsapi", methods=["GET", "POST"])
def resultsapi():
    results = StudentResult.query.all()
    results_list = []
    print("resultsapi")

    if results:
        for result in results:
            payload = {
                "id": result.id,
                "name": result.student.name,
                "subject": result.subject.name,
                "result": result.result,
                "completed_year": result.student.completed_year,
                "index_number": result.index_number
                
            }
            results_list.append(payload)

        context = {
            "status": True,
            "message": " result found!",
            "data": results_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "result not found",
            "error": "null"
        }

        return jsonify(context), 404

@core.route("/studentapi/<int:id>", methods=["GET", "POST"])
def studentapi(id):
    user = User.query.filter_by(id=id).first()
    results = StudentResult.query.filter_by(index_number=user.index_number).all()
    results_list = []
    print("studenting")
    print(user)
    print(results)

    if results:
        for result in results:
            payload = {
                "id": result.id,
                "name": user.name,
                "subject": result.subject.name,
                "result": result.result,
                "completed_year": result.student.completed_year,
                "index_number": result.index_number
                
            }
            results_list.append(payload)

        context = {
            "status": True,
            "message": " result found!",
            "data": results_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "result not found",
            "error": "null"
        }

        return jsonify(context), 404


# @core.route("/report", methods=["GET"])
# @login_required
# def report():
#     return render_template("agentportal/report.html")



# @core.route('/ig', methods=['GET', 'POST'])
# # @require_api_key
# def checkresult():
#     form = CheckResultForm()
#     if request.method =="POST":
#         user = User.query.filter_by(index_number=form.index_number.data).first()
#         print(form.index_number.data)
#         print(form.year.data)
#         print(user)
#         # result = StudentResult.query.filter_by(id=form.index_number.data).first()
#         results = StudentResult.query.filter_by(index_number=form.index_number.data, year=form.year.data).all()
#         print(result)
#         return render_template("viewresult.html",results=results,user=user)
#     return render_template("index.html",form=form)


@core.route("/checkresultsapi", methods=["GET"])
def checkresultsapi():
    form = CheckResultForm()
    ting = request.args.get("year")
    print(ting)
    # results = StudentResult.query.all()
    results_list = []
    if request.method=='GET':
        results = StudentResult.query.filter_by(index_number=form.index_number.data, year=form.year.data).all()
        print(form.index_number.data)
        print(form.year.data)
        print("results:")
        print(results)
        if results:
            print("works")


            for result in results:
                payload = {
                    "id": result.id,
                    "name": result.name,
                    "subject": result.subject.name,
                    "result": result.result,
                    "index_number":result.index_number
                    
                }
                results_list.append(payload)
                print(results_list)
                print("results_list")

            context = {
                "status": True,
                "message": " result found!",
                "data": results_list,
            }
            print("context")
            print(context)

            return jsonify(context), 200
        else:
            print("not working")
            context = {
                "status": False,
                "message": "results not found",
                "error": "null"
            }

            return jsonify(context), 404

# @core.route("/api/logs", methods=["GET", "POST"])
# def logs():
#     logs = EcomRequest.query.order_by(desc(EcomRequest.date))
#     payload_list = []

#     for log in logs:
#         payload = {
#             "id": log.id,
#             "farmerName": log.farmers.last_name if log.farmer_id else "N/A",
#             "farmercode": log.farmers.farmercode if log.farmer_id else "N/A",
#             "cashcode": log.farmers.cashcode if log.farmer_id else "N/A",
#             "premiumAmount": log.farmers.premium_amount if log.farmer_id else "N/A",
#             "number": log.number,
#             "disposition": log.disposition,
#             "timestamp": log.date,
#             "smsDisposition": log.sms_disposition,

#         }
#         payload_list.append(payload)

#     context = {
#         "status": True,
#         "message": " Farmer  found!",
#         "data": payload_list
#     }

#     return jsonify(context), 200




@core.route('/uploadfarmer', methods=['GET', 'POST'])
@login_required
def uploadfarmer():
    form = FarmerForm()
    user = User.query.filter_by(email=session['email']).first()
    session.pop('msg', None)

    data = []

    if form.validate_on_submit():
        session.pop('csv_data', None)
        session.pop('uploaded_farmers', None)
        session.pop('duplicates', None)

        if form.uploadfile.data:
            uploaded_file = request.files['uploadfile']

            # Generate a unique name for the uploaded file
            unique_file_name = str(uuid4()) + uploaded_file.filename
            filepath = os.path.join(current_app.root_path, unique_file_name)

            uploaded_file.save(filepath)
            session['current_file'] = filepath
            return redirect(url_for('core.uploadsummary'))

    return render_template('agentportal/uploadfarmer.html', form=form, user=user, data=data)


@core.route('/uploadsummary', methods=['GET', 'POST'])
def uploadsummary():
    form = FarmerForm()
    filepath = session.get('current_file')
    upload_data = []

    with open(filepath, encoding='ISO-8859-1') as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            upload_data.append(row)

        data = upload_data

    if request.method == 'POST':
        uploaded = []
        duplicates = []
        line_count = 0

        for i in range(0, len(data)):
            farmer = Farmer.query.filter_by(number=data[i][4]).first()

            if farmer:
                duplicates.append(data[i])
            else:
                try:
                    farmers_save = Farmer(
                        cooperative=data[i][0],
                        farmercode=data[i][1],
                        last_name=data[i][2],
                        society=data[i][3],
                        number=data[i][4],
                        premium_amount=data[i][5],
                        language=data[i][6],
                        cashcode=data[i][7],
                        country=data[i][8],
                        first_name="NA",
                        location="NA"
                    )

                    db.session.add(farmers_save)
                    db.session.commit()
                    uploaded.append(data[i])
                except Exception as e:
                    # Add the line number to the error message
                    error_message = f"Error on line {line_count}: {str(e)}"

                    # Handle the error appropriately
                    message = error_message
                    session.pop('csv_data', None)
        session['uploaded_farmers'] = uploaded
        session['duplicates'] = duplicates

        os.remove(filepath)
        session.pop('current_file')

        return render_template(
            'agentportal/uploadsummarydetails.html',
            len_added=len(uploaded), uploaded=uploaded,
            len_duplicates=len(duplicates), duplicates=duplicates
        )

    return render_template('agentportal/uploadsummary.html', len_added=len(data), data=data, form=form)

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=resend_sms, trigger="interval", seconds=600)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
