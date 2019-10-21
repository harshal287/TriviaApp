import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in questions]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = paginate_questions(request,categories)
    allcategories = []
    for category in categories:
        allcategories.append(category.type)
    if len(formatted_categories) == 0:
      abort(404)
    return jsonify({
      'categories': allcategories
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
  @app.route('/questions', methods=['GET'])
  def get_questions():
    if request.method == 'GET':
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = paginate_questions(request,questions)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = paginate_questions(request,categories)
        allcategories = []
        for category in categories:
            allcategories.append(category.type)
        if len(formatted_questions) == 0:
          abort(404)
        return jsonify({
          'success': 'True',
          'questions': formatted_questions,
          'totalQuestions':len(Question.query.all()),
          'categories': allcategories
        })

  


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    body = request.get_json()
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      categories = Category.query.order_by(Category.id).all()
      formatted_categories = paginate_questions(request,categories)
      allcategories = []
      for category in categories:
          allcategories.append(category.type)

      return jsonify({
        'success': 'True',
        'deleted':question_id,
        'questions':current_questions,
        'totalQuestions':len(Question.query.all()),
        'categories': allcategories,
        'currentCategory': 'Art'
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category',None)
    new_difficulty = body.get('difficulty',None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      categories = Category.query.order_by(Category.id).all()
      formatted_categories = paginate_questions(request,categories)
      allcategories = []
      for category in categories:
        allcategories.append(category.type)

      return jsonify({
        'success': 'True',
        'created':question.id,
        'questions':current_questions,
        'totalQuestions':len(Question.query.all()),
        'categories': allcategories,
        'currentCategory': 'Art'
      })
    except:
      abort(422)
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questionSearch', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
    formatted_questions = paginate_questions(request,questions)
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = paginate_questions(request,categories)
    allcategories = []
    for category in categories:
        allcategories.append(category.type)    
    if len(formatted_questions) == 0:
      abort(404)
    return jsonify({
        'success': 'True',
        'questions':formatted_questions,
        'totalQuestions':len(Question.query.all()),
        'categories': allcategories,
        'currentCategory': 'Art'
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_specific_category(id):
    category = Category.query.filter_by(id = id)
    for cat in category:
      catId = cat.id
    questions = Question.query.filter(Question.category == catId)
    formatted_questions = paginate_questions(request,questions)
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = paginate_questions(request,categories)
    allcategories = []
    for category in categories:
        allcategories.append(category.type)
    if len(formatted_questions) == 0:
      abort(404)
    return jsonify({
      'success': 'True',
      'questions': formatted_questions,
      'totalQuestions':len(Question.query.all()),
      'categories': allcategories,
      'currentCategory': 'Art'
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
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    body = request.get_json()
    quizCategory = body.get('quizCategory', None)
    previousQuestions = body.get('previousQuestions', None)
    currentQuestion = {"answer":"Escher","category":2,"difficulty":1,"id":16,"question":"Where is Taj Mahal?"}
    #currentQuestion = "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    previousQuestions = [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }]
    
    '''
    CategoryQuiz = Category.query.filter_by(type = quizCategory)
    
    for cat in CategoryQuiz:
      catId = cat.id
    questions = Question.query.filter(Question.category == catId)
    formatted_questions = paginate_questions(request,questions)
    for catergoryID in CategoryQuiz:
        id = catergoryID.id
    questions = Question.query.filter(Question.category==id)
    formatted_questions = paginate_questions(request,questions)  
    currentQuestion = Question.query.get(5)
    if len(formatted_questions) == 0:
      abort(404)
    
    return jsonify({
        'success': 'True',
        'previousQuestions':formatted_questions,
        'currentQuestion':CurrentQuestion
    })
    '''
    return jsonify({
        'showAnswer': 'false',
        'success': 'True',
        'currentQuestion': currentQuestion,
        'previousQuestions': previousQuestions,
    })
  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    