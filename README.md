# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories, success value
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true
    }
```

#### GET /questions
- General:
    - Returns a list of questions, success value, total questions and list of categories.
    - The questions are listed 10 per page
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current category": 1,
  "questions": [
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
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
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
    }
  ],
  "success": true,
  "total_questions": 23
}
```
#### GET /questions?page={pageno}

- General:
    - Returns the questions from the page specified
    - Returns a list of questions, success value, total questions and list of categories.

- Sample: `curl http://127.0.0.1:5000/questions?page=2`

```{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current category": 1,
  "questions": [
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Seven",
      "category": 4,
      "difficulty": 1,
      "id": 25,
      "question": "How many wonders are there in the world?"
    },
    {
      "answer": "white",
      "category": 1,
      "difficulty": 1,
      "id": 29,
      "question": "What is the blood color for cockroach"
    },
    {
      "answer": "V.Ramakrishnan",
      "category": 1,
      "difficulty": 1,
      "id": 31,
      "question": "Who is the Indian Scientist won Nobel prize in 2009?"
    },
    {
      "answer": "8",
      "category": 1,
      "difficulty": 1,
      "id": 33,
      "question": "how many legs for spider?"
    }
  ],
  "success": true,
  "total_questions": 23
}
```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions for the selected category, success value, total questions and category id of the selected category.
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```{
  "currentCategory": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
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
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```
#### DELETE /questions/{quesion_id}
- General:
    - Delete the question which matches the given question_id if it exists and returns success value
    - If the question_id doesn't exists, returns 404 resource not found error.
- Sample: `curl -X DELETE "http://127.0.0.1:5000/questions/5"`

```{
  "success": true
}
```
#### POST /questions
- General:
    - Creates a new question using the question, answer, difficulty and category.
    - Returns success value and id of the created question
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"Who is the discoverer of hydrogen?\",\"answer\":\"Cavendish\",\"difficulty\":\"2\",\"category\":\"4\"}" http://127.0.0.1:5000/questions`

```{
  "created": 36,
  "success": true
}
```
#### POST /questionsearch
- General:
    - Search all the questions containing the given search term.
    - Returns a list of questions containing the given search term, success value, total questions and category id as None.
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"Who\"}" http://127.0.0.1:5000/questionsearch`

```{
  "currentCategory": null,
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "V.Ramakrishnan",
      "category": 1,
      "difficulty": 1,
      "id": 31,
      "question": "Who is the Indian Scientist won Nobel prize in 2009?"
    },
    {
      "answer": "Cavendish",
      "category": 4,
      "difficulty": 2,
      "id": 36,
      "question": "Who is the discoverer of hydrogen?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```
#### POST /quizzes
- General:
    - List a random question which is not a previously displayed question.
    - Gets previous quesion ID and category selected
    - Returns a question and success value
- Sample: `Curl -X POST -H "Content-Type: application/json" -d  "{\"previous_questions\":\"3\",\"quiz_category\": {\"type\": \"click\",\"id\":0}}"  http://127.0.0.1:5000/quizzes`

```{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
> View the [Frontend README](./frontend/README.md) for more details.
