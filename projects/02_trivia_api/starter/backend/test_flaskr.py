import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'Why does the caged bird sing?',
            'answer': 'Because it has nothing better to do',
            'difficulty': 5,
            'category': 1
        }
        self.bad_question = {
            'question': 'Why does the caged bird sing?',
            'answer': 'Because it has nothing better to do',
            'difficulty': 5,
            'category': 'History'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_delete_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        deleted_id = data["questions"][0]["id"]
        res_deleted = self.client().delete(f'/questions/{deleted_id}')
        data_deleted = json.loads(res.data)

        self.assertEqual(res_deleted.status_code, 200)
        self.assertEqual(data_deleted['success'], True)

    def test_create_question(self):
        res = self.client().post('/addquestions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_all_questions(self):
        res = self.client().post('/questions', json={'searchTerm':  'title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_get_all_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions':  [],
            'quiz_category': {
                'id': 2
            }})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))

    def test_400_question_does_not_have_body(self):
        res = self.client().post('/addquestions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/question')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_422_question_does_not_exist(self):
        res = self.client().post('/addquestions', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_500_failed_search_question(self):
        res = self.client().post('/questions', json={'search_term':  'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
