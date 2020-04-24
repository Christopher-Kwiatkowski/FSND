import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow+
    '''
    @app.after_request
    def after_request(response):
        # response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-All-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def all_categories():
        categories = Category.query.all()
        # print(f'Output {categories[0].type}')
        jsonified = {}
        for category in categories:
            jsonified[f'{category.id}'] = category.type
        # print(jsonified)
        return jsonify({
            'success': True,
            'categories': jsonified
        })
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        categories = Category.query.all()
        count = 0
        for question in questions:
            count += 1
        formatted_questions = [question.format() for question in questions]
        jsonified_categories = {}
        print(count)
        for category in categories:
            jsonified_categories[f'{category.id}'] = category.type
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': count,
            'categories': jsonified_categories,
            'current_category': 'test'
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        selected_question = Question.query.get(question_id)
        selected_question.delete()

        return jsonify({
            'success': True
        })
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/addquestions', methods=['POST'])
    def add_question():
        new_question = json.loads(request.data)
        question = new_question['question']
        answer = new_question['answer']
        difficulty = int(new_question['difficulty'])
        category = int(new_question['category'])

        Question(question, answer, category, difficulty).insert()
        return jsonify({
            'success': True
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions', methods=["POST"])
    def search_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        search_term = json.loads(request.data)
        search_term_lower = search_term['searchTerm'].lower()
        questions = Question.query.all()
        count = 0
        data = []
        for question in questions:
            if search_term_lower in question.question.lower():
                count += 1
                data.append(question.format())
        return jsonify({
            'success': True,
            'questions': data[start:end],
            'total_questions': count,
            'current_category': 'test'
        })
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.filter_by(category=category_id).all()
        category = Category.query.get(category_id)
        count = 0
        for question in questions:
            count += 1
        formatted_questions = [question.format() for question in questions]
        jsonified_category = {}
        jsonified_category[f'{category.id}'] = category.type
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': count,
            'current_category': jsonified_category
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
