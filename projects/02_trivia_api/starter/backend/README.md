# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers. +
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.+
3. Create an endpoint to handle GET requests for all available categories.+
4. Create an endpoint to DELETE question using a question ID.+
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.+
6. Create a POST endpoint to get questions based on category.+
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.+
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.+
9. Create error handlers for all expected errors including 400, 404, 422 and 500.+

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/addquestions'
POST '/questions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of dictionaries of questions in which the keys are the descriptors for the values, being the 'ID' of the question, 'question' itself, 'answer' to the question, 'category' of the question, and 'difficulty' of the question. Also returns the total number of questions, the categories available, and the current category. The value is the id number, string of the question, string of the answer, integer of the difficulty from 1-5, integer corresponding to the catagory, integer for the total number of questions, an object containing the key value pairs of category with string of category, and string of current category respectively.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'questions': {'id':1
              'question':"What is love"
              'answer':"A night at the roxbury"
              'category': 4
              'difficulty': 1
},
'total_questions': 20,
'categories': {'1' : "Science",
              '2' : "Art",
              '3' : "Geography",
              '4' : "History",
              '5' : "Entertainment",
              '6' : "Sports"},
'current_category': 'category'}

DELETE '/questions/<int:question_id>'
- Deletes a question corresponding to the imput argument (id in this case)
- Request Arguments: Id of question to be deleted (integer)
- Returns: An Success or failure.

POST '/addquestions'
- Creates a new question taking in an object with the new question, answer, category, and difficulty (see return for GET '/questions' for example).
- Request Arguments: An object with the new question, answer, category, and difficulty.
- Returns: Success or failure of the operation.

POST '/questions'
- Searches through the questions in the database based on an input to sort by and returns a list of all question objects that contain the search term in the question, the total number found, and the category.
- Request Arguments: The search term that we want to find questions that contain said term.
- Returns: A list of all found questions matching the search criteria, the total in an integer of found questions, and the category.
{'questions': {'id':1
              'question':"What is love"
              'answer':"A night at the roxbury"
              'category': 4
              'difficulty': 1
},
'total_questions': 20,
'category': 'category'

GET '/categories/<int:category_id>/questions'
- Fetches a list of all questions that are in the category being searched for.
- Request Arguments: The category id to search for.
- Returns: A list of all found questions matching the category criteria, the total in an integer of found questions, and the category.
{'questions': {'id':1
              'question':"What is love"
              'answer':"A night at the roxbury"
              'category': 4
              'difficulty': 1
},
'total_questions': 20,
'category': '{'1': 'Science'}'

POST '/quizzes'
- Fetches a list of all questions that are in the category being searched for, or all questions if no category is specified. The questions are delivered one at a time and randomized until there are no more questions that have not been seen already.
- Request Arguments: A list of all already seen ids for questions and a category for questions to serve up.
- Returns: A question object.
{'questions': {'id':1
              'question':"What is love"
              'answer':"A night at the roxbury"
              'category': 4
              'difficulty': 1
}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
