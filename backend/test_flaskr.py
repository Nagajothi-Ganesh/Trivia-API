import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()

my_id = os.getenv('ID')
key = os.getenv('SECRET_KEY')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(my_id, key,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    
    def test_404_sent_requesting_category_with_ID(self):
        res = self.client().get("/categories/02")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")   

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))   
        self.assertTrue(data["total_questions"])  
        self.assertTrue(len(data["categories"]))  

    def test_delete_questions_with_id(self):
        res = self.client().delete("/questions/4")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_404_sent_requesting_not_present_question(self):
        res = self.client().delete("/questions/999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")  

    def test_add_question(self):
        new_question = {"question": "Who is known as the Father of Indian Space Program", "answer": "Vikrama Sarabhai", "difficulty": 2, "category": 1}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])  
    
    def test_400_add_question_without_few_inputfields(self):
        err_question = {"question": "Who is known as the Father of Indian Space Program", "answer": "Vikrama Sarabhai", "difficulty": 2}
        res = self.client().post("/questions", json=err_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "bad request")   

    def test_search_questions(self):
        res = self.client().post("/questionsearch", json={ "searchTerm": "Which" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))   
        self.assertTrue(data["totalQuestions"])  
        self.assertEqual(data["currentCategory"], None)

    def test_422_search_questions_with_invalid_text(self):
        res = self.client().post("/questionsearch", json={"searchTerm": "searchTerm" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "bad request")  
    
    def test_list_questions_by_category_(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))   
        self.assertTrue(data["totalQuestions"])  
        self.assertEqual(data["currentCategory"],2)    

    def test_404_list_questions_with_invalid_category(self):
        res = self.client().get("/categories/8/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")  

    def test_play_quiz(self):
        res = self.client().post("/quizzes", json={ "previous_questions": "3", "quiz_category": {'type': 'click', 'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]))   

    def test_422_play_quiz_without_category(self):
        res = self.client().post("/quizzes", json={ "previous_questions": "3"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "unprocessable")  
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()