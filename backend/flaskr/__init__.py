"""
Backend program for Trivia API
"""
import random
from flask_cors import CORS
from flask import Flask, request, abort, jsonify
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()

            if len(categories) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "categories": {item.id: item.type for item in categories},
                }
            )
        except Exception as error:
            print(error)
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated, ten questions
    per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).paginate(per_page=QUESTIONS_PER_PAGE)
            questions = [question.format() for question in selection.items]
            categories_sel = Category.query.order_by(Category.id).all()
            if len(questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(Question.query.all()),
                    "categories": {item.id: item.type for item in categories_sel},
                    "current category": 1,
                }
            )
        except Exception as error:
            print(error)
            abort(404)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):

        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            question.delete()

            return jsonify(
                {
                    "success": True,
                }
            )
        except Exception as error:
            print(error)
            abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def add_questions():

        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            if (new_question is None or new_answer is None or new_category is None):
                abort(400)

            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify(
             {
                 "success": True,
                 "created": question.id
             }
            )

        except Exception as error:
            print(error)
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questionsearch", methods=["POST"])
    def search_questions():
        body = request.get_json()
        searchTerm = body.get("searchTerm", None)
        try:
            selection = Question.query.filter(Question.question.ilike("%{}%".format(searchTerm))).order_by(Question.id).paginate(per_page=QUESTIONS_PER_PAGE)
            questions = [question.format() for question in selection.items]

            if len(questions) == 0:
                raise KeyError

            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "totalQuestions": len(questions),
                    "currentCategory": None,
                }
            )
        except KeyError:
            abort(400)
        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def question_categories(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).order_by(Question.id).paginate(per_page=QUESTIONS_PER_PAGE)
            questions = [question.format() for question in selection.items]

            if len(questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "totalQuestions": len(questions),
                    "currentCategory": category_id
                }
            )
        except Exception as error:
            print(error)
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_quizzes():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions', None)
            category = body.get('quiz_category')
            if category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:
                questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            new_question = [question.format() for question in questions]
            if len(new_question) > 0:
                next_question = (random.choice(new_question))
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            }

            )
        except Exception as error:
            print(error)
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    return app

