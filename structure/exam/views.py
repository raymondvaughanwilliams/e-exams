import atexit
import csv
import os
from os import environ
from uuid import uuid4
import secrets
import random
import string
import requests
from requests.auth import HTTPBasicAuth
# from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, Blueprint, session, redirect, url_for, jsonify, current_app, request 
from flask_login import login_required
from sqlalchemy import and_, or_, desc
from flask_mail import Mail, Message
from datetime import date,datetime
from structure import db,mail ,photos,app
# from structure.core.forms import FilterForm,SipRequestForm , IssueForm,NumberSearchForm,ExtForm
# from structure.about.forms import AboutForm
from werkzeug.utils import secure_filename
from structure.models import Exam,Question,Answer ,Submission ,Photo ,Images
from PIL import Image
# import pytesseract 
# from io import BytesIO
# import base64
from random import shuffle

exam = Blueprint('exam', __name__)

def generate_random_number():
    return random.randint(1000, 9999)

# Function to generate a random string
def generate_random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Modify the function to generate a unique Jitsi room ID
def generate_unique_jitsi_room_id(exam_name):
    random_number = generate_random_number()
    random_string = generate_random_string()
    return f'{exam_name}_{random_string}_{random_number}'


@exam.route('/exams')
def exams():
    print('shgdkhldjs')
    exams = Exam.query.all()
    # exams = Exam.query.filter_by(status="active").all()
    return render_template('exam/exams.html', exams=exams)

# @exam.route('/exams/<int:exam_id>/questions', methods=['GET', 'POST'])
# def questions(exam_id):
#     exam = Exam.query.get_or_404(exam_id)
#     questions = Question.query.filter_by(exam_id=exam_id).all()
#     print(questions)
#     submission = Submission.query.filter_by(user_id=session['id'], exam_id=exam_id).first()
#     if submission:
#         return redirect(url_for('exam.view_results', submission_id=submission.question_id))
#     if request.method == 'POST':
#         exam_id = request.form.get('exam_id')
#         question_id = request.form.get('question_id')
#         answer_id = request.form.get('answer_id')
#         print('tings',exam_id,question_id,answer_id)

#         submission = Submission(user_id=session['id'], exam_id=exam_id, question_id=question_id, answer_id=answer_id)
#         db.session.add(submission)
#         db.session.commit()

#         session['msg'] = 'Exam submitted successfully'

#         return redirect(url_for('exam.view_results', submission_id=submission.id))
    
#     return render_template('exam/questions.html', exam=exam, questions=questions)


@exam.route('/exams/<int:exam_id>/questions', methods=['GET', 'POST'])
def questions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()

    if request.method == 'POST':
        # Retrieve exam ID from the form data
        # exam_id = request.form.get('exam_id')

        # Initialize a list to store the submitted answers
        submissions = []

        # Iterate through the questions to retrieve submitted answers
        for question in questions:
            # Retrieve question ID and submitted answer ID from the form data
            question_id = request.form.get(f'question_{question.id}')
            answer_id = request.form.get(f'answer_{question.id}')

            print(question_id, answer_id)

            # Check if both question ID and answer ID are provided
            if question_id is not None and answer_id is not None:
                # print(question_id, answer_id)
                # Create a submission instance and add it to the list
                submission = Submission(
                    user_id=session['id'],
                    exam_id=exam_id,
                    question_id=question_id,
                    answer_id=answer_id
                )
                submissions.append(submission)

        # Add all submissions to the database session and commit changes
        print(submissions)
        db.session.add_all(submissions)
        db.session.commit()

        # Redirect to view results page after submitting the exam'
        print(exam_id)
        return redirect(url_for('exam.view_results', exam_id=exam_id,user_id=session['id']))

    return render_template('exam/questions.html', exam=exam, questions=questions)



@exam.route('/questions/<int:question_id>/answers')
def view_answers(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id).all()
    return render_template('answers.html', question=question, answers=answers)

@exam.route('/add_submission', methods=['GET', 'POST'])
def add_submission():
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        question_id = request.form.get('question_id')
        answer_id = request.form.get('answer_id')
        print(question_id,answer_id,exam_id)

        submission = Submission(user_id=session['user_id'], exam_id=exam_id, question_id=question_id, answer_id=answer_id)
        db.session.add(submission)
        db.session.commit()

        session['msg'] = 'Exam submitted successfully'
        print(session['msg'])

        return redirect(url_for('exam.view_results', exam_id=exam_id))  # Redirect to the same page after adding submission

    # If GET request, render the add submission form
    # users = User.query.all()  # Fetch all users to populate dropdown
    exams = Exam.query.all()  # Fetch all exams to populate dropdown
    questions = Question.query.all()  # Fetch all questions to populate dropdown
    answers = Answer.query.all()  # Fetch all answers to populate dropdown
    return render_template('add_submission.html', exams=exams, questions=questions, answers=answers)



@exam.route('/view_results/<int:exam_id>/<int:user_id>')
def view_results(exam_id, user_id):
    # Retrieve user ID from session
    session_user_id = session.get('id')
    
    # Check if user is logged in
    if session_user_id is None:
        return "User not logged in"  # You might want to handle this case differently

    # Count total number of questions in the exam
    total_questions = Question.query.filter_by(exam_id=exam_id).count()

    # Count number of correct answers for the user in the exam
    correct_answers = db.session.query(Submission).\
                        join(Question, Submission.question_id == Question.id).\
                        join(Answer, Submission.answer_id == Answer.id).\
                        filter(Submission.user_id == user_id).\
                        filter(Submission.exam_id == exam_id).\
                        filter(Answer.is_correct == True).\
                        count()

    # Calculate percentage
    if total_questions > 0:
        percentage = (correct_answers / total_questions) * 100
    else:
        percentage = 0

    return render_template('exam/view_result.html', percentage=percentage)




# @app.route('/questions')
# def get_questions():
#     questions = Question.query.all()
#     return jsonify([{'id': q.id, 'text': q.text} for q in questions])

# @app.route('/answers/<int:question_id>')
# def get_answers(question_id):
#     answers = Answer.query.filter_by(question_id=question_id).all()
#     return jsonify([{'id': a.id, 'text': a.text} for a in answers])

# @app.route('/submit', methods=['POST'])
# def submit_exam():
#     answers = request.json.get('answers')  # Expecting {'answers': [{'question_id': 1, 'text': 'Answer to Q1'}, ...]}
#     for ans in answers:
#         new_answer = Answer(question_id=ans['question_id'], text=ans['text'])
#         db.session.add(new_answer)
#     db.session.commit()
#     return jsonify({'message': 'Exam submitted successfully'}), 201




# @exam.route('/create_dummy_data')
# def create_dummy_data():
#     # Create dummy exams
#     exam1 = Exam(name='Math Exam')
#     exam2 = Exam(name='Science Exam')
#     db.session.add(exam1)
#     db.session.add(exam2)
#     db.session.commit()

#     # List of questions with their answers
#     questions_data = [
#         {
#             'exam_id': exam1.id,
#             'question_text': 'What is the capital of France?',
#             'answers': ['Paris', 'London', 'Berlin', 'Rome'],
#             'correct_answer_index': 0  # Index of correct answer in the answers list
#         },
#         {
#             'exam_id': exam1.id,
#             'question_text': 'What is 10 multiplied by 5?',
#             'answers': ['20', '30', '50', '100'],
#             'correct_answer_index': 2
#         },
#         {
#             'exam_id': exam2.id,
#             'question_text': 'What is the chemical symbol for water?',
#             'answers': ['H2O', 'CO2', 'O2', 'NaCl'],
#             'correct_answer_index': 0
#         },
#         {
#             'exam_id': exam2.id,
#             'question_text': 'What is the powerhouse of the cell?',
#             'answers': ['Mitochondria', 'Nucleus', 'Ribosome', 'Golgi apparatus'],
#             'correct_answer_index': 0
#         },
#         # Add more questions here as needed
#     ]

#     # Shuffle the order of questions
#     shuffle(questions_data)

#     for question_data in questions_data[:10]:  # Select first 10 questions
#         # Create the question
#         question = Question(exam_id=question_data['exam_id'], question_text=question_data['question_text'])
#         db.session.add(question)
#         db.session.commit()

#         # Create answers for the question
#         for i, answer_text in enumerate(question_data['answers']):
#             is_correct = i == question_data['correct_answer_index']
#             answer = Answer(question_id=question.id, answer_text=answer_text, is_correct=is_correct)
#             db.session.add(answer)
#             db.session.commit()

#     return jsonify({'message': 'Dummy data created successfully'})



@exam.route('/invigilator/exams')
def iexams():
    print('shgdkhldjs')
    exams = Exam.query.all()
    # exams = Exam.query.filter_by(status="active").all()
    return render_template('exam/invigilator/exams.html', exams=exams)


@exam.route('/invigilator/examresults/<int:exam_id>')
def iresults(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    results = Submission.query.filter_by(exam_id=exam_id).all()
    return render_template('exam/invigilator/results.html', exam=exam , results=results)



@exam.route('/invigilator/exam/<int:exam_id>', methods=['GET', 'POST'])
def add_question(exam_id):
    if request.method == 'POST':
        # exam_id = request.form.get('exam_id')
        question_text = request.form.get('question_text')
        answers = request.form.getlist('answer')  # Get all submitted answers
        correct_answer_index = int(request.form.get('correct_answer_index'))

        # Create the question
        question = Question(exam_id=exam_id, question_text=question_text)
        db.session.add(question)
        db.session.commit()

        # Create answers for the question
        for i, answer_text in enumerate(answers):
            is_correct = i == correct_answer_index
            answer = Answer(question_id=question.id, answer_text=answer_text, is_correct=is_correct)
            db.session.add(answer)
        
        db.session.commit()

        return redirect(url_for('exam.add_question',exam_id=exam_id))  # Redirect to the same page after adding question

    # If GET request, render the add question form
    exams = Exam.query.all()  # Fetch all exams to populate dropdown
    exam = Exam.query.get(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    return render_template('exam/invigilator/exam.html', exams=exams ,exam=exam, questions=questions)

@exam.route('/invigilator/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.question_text = request.form['question_text']
        
        # Update answers
        for answer in question.answers:
            answer_text = request.form.get(f'answer_{answer.id}')
            if answer_text is not None:
                answer.answer_text = answer_text
        
        db.session.commit()
        return redirect(url_for('exam.add_question', exam_id=question.exam_id))
    return render_template('exam/invigilator/edit_question.html', question=question)

@exam.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('exam.add_question'))



@exam.route('/invigilator/create_exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        exam_name = request.form.get('exam_name')
        # Create exam in the database
        exam = Exam(name=exam_name)
        db.session.add(exam)
        db.session.commit()

        # Generate unique Jitsi room ID
        jitsi_room_id = generate_unique_jitsi_room_id(exam.id)
        # Store the Jitsi room ID in the database
        exam.jitsi_room_id = jitsi_room_id
        db.session.commit()

        # Redirect to the exam page with the Jitsi room ID
        return redirect(url_for('exam.add_question', exam_id=exam.id))

    return render_template('exam/invigilator/create_exam.html')


@exam.route('/invigilator/examroom/<int:exam_id>')
def exam_room(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    jitsi_room_id = exam.jitsi_room_id
    return render_template('exam/invigilator/exam_room.html', jitsi_room_id=jitsi_room_id)


from werkzeug.datastructures import FileStorage
import base64
from tempfile import NamedTemporaryFile
@exam.route('/save_picture', methods=['POST'])
def save_picture():
    data = request.json
    image_data = data.get('image_data')
    exam_id = data.get('exam_id')
    print("exam_id", exam_id)

    if image_data:
        # Decode base64 image data
        image_data = base64.b64decode(image_data.split(',')[1])

        # Create a temporary file to save the image data
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(image_data)
        temp_file.close()

        # Define the upload directory
        fpath = "structure/static/images/packages/"

        # Ensure the directory exists
        if not os.path.exists(fpath):
            os.makedirs(fpath)

        # Generate a unique filename
        filename = secrets.token_hex(10) + ".png"

        # Move the temporary file to the uploads destination with the unique filename
        os.rename(temp_file.name, os.path.join(fpath, filename))

        # Save image path to database
        image_path = "static/images/packages/" + filename
        print("image_path", image_path)
        
        # Ensure user is logged in and has an ID
        if 'id' in session:
            # Save image path to database along with user ID
            photo = Photo(image_location=image_path, user_id=session['id'], exam_id=exam_id)
            db.session.add(photo)
            db.session.commit()

            return jsonify({'message': 'Picture saved successfully', 'image_path': image_path}), 200
        else:
            return jsonify({'error': 'User not logged in'}), 400
    else:
        return jsonify({'error': 'No image data received'}), 400




@exam.route('/infractions/<int:exam_id>', methods=['POST','GET'])
def infractions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    infractions = Photo.query.filter_by(exam_id=exam_id).all()
    return render_template('exam/invigilator/infractions.html', exam=exam, infractions=infractions)








# @exam.route('/upload_image', methods=['POST'])
# def upload_image():
#     """
#     Endpoint for uploading an image.
    
#     This function expects a POST request with JSON data containing an 'image' field.
#     The contents of the 'image' field are saved to a file or processed as needed.
    
#     Returns:
#         None
#     """
#     # Print a message to indicate that the image is being uploaded
#     print('Image uploading')
    
#     # Retrieve the image data from the request JSON
#     image_data = request.json['image']
    
#     # : Save the image data to a file or process it as needed
#     # ...
#     return jsonify({'success': True})
# Register the blueprint
