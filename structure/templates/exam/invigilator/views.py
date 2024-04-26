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
from structure.models import Exam,Question,Answer ,Submission
from PIL import Image
# import pytesseract 
# from io import BytesIO
# import base64
from random import shuffle

exam = Blueprint('exam', __name__)




@exam.route('/exams')
def exams():
    print('shgdkhldjs')
    exams = Exam.query.all()
    # exams = Exam.query.filter_by(status="active").all()
    return render_template('exam/exams.html', exams=exams)

@exam.route('/exams/<int:exam_id>/questions', methods=['GET', 'POST'])
def questions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    print(questions)
    submission = Submission.query.filter_by(user_id=session['id'], exam_id=exam_id).first()
    if submission:
        return redirect(url_for('exam.view_results', question_id=submission.question_id))
    if request.method == 'POST':
        exam_id = request.form.get('exam_id')
        question_id = request.form.get('question_id')
        answer_id = request.form.get('answer_id')

        submission = Submission(user_id=session['id'], exam_id=exam_id, question_id=question_id, answer_id=answer_id)
        db.session.add(submission)
        db.session.commit()

        session['msg'] = 'Exam submitted successfully'

        return redirect(url_for('exam.view_results', exam_id=exam_id))
    
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



@exam.route('/view_results/<int:exam_id>')
def view_results(exam_id):
    user_id = session.get('user_id')
    if user_id is None:
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

    return render_template('view_results.html', percentage=percentage)



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
    return render_template('exam/invigilator/addquestions.html', exams=exams ,exam=exam, questions=questions)

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

# Register the blueprint
