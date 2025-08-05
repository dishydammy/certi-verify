# Hashproof ML System - Backend Integration Guide

## Overview
The ML System is a simple API service that generates tests for programming languages and grades student submissions using AI. It runs as a separate service that can be called to handle all assessments logic.

What it does:

✅ Generates tests (MCQ, Code) for a specified programming language (e.g Python, JavaScript)
✅ Grades student answers automatically
✅ Returns pass/fail status for NFT minting
✅ Provides detailed feedback and scores


## API Endpoints

1. Generate a Code Test
> Endpoint: POST /generate_code_test
 
> Purpose: Ask the AI to generate a set of coding questions.

> Request Body (JSON):

```
{
  "difficulty": "beginner",
  "question_count": 3,
  "topic": "JavaScript"
}
```

> Response:

```
{
  "test_id": "848d7d9f-d31e-436f-9972-23f2b87c7b8c",
  "type": "code",
  "topic": "JavaScript",
  "difficulty": "beginner",
  "questions": [
    {
      "id": "javascript_code_1",
      "question": "Write a function that doubles a number...",
      "template": "function double(num) { ... }",
      "points": 5,
      "test_cases": [ ... ]
    },
    ...
  ],
  "total_points": 15,
  "question_count": 3
}
```

**Important: The entire questions array returned from this endpoint need to be stored in a database. This is critical for grading later, as the grading endpoint needs the original question data.**

2. Grade a Code Test
> Endpoint: POST /grade_code_test

> Purpose: Submit a student's answers to be graded by the AI.

> Request Body (JSON):

```
{
  "student_id": "student-123",
  "test_id": "848d7d9f-d31e-436f-9972-23f2b87c7b8c",
  "code_answers": [
    {
      "question_id": "javascript_code_1",
      "code": "function double(num) { return num * 2; }"
    },
    ...
  ]
}
```

> How it Works: The service uses the test_id to retrieve the original questions from our in-memory TEST_STORAGE. It then sends the student's code and the original question to the AI for grading.

> Response (JSON): The final score and detailed feedback.

```
{
  "student_id": "student-123",
  "test_id": "848d7d9f-d31e-436f-9972-23f2b87c7b8c",
  "overall_score": 0.95,
  "total_points": 14,
  "max_possible_points": 15,
  "passed": true,
  "feedback": [
    {
      "question_id": "javascript_code_1",
      "score": "10/10",
      "points_earned": 5,
      "max_points": 5,
      "feedback": "SCORE: 10/10\nExcellent work. The code is clean..."
    },
    ...
  ]
}
```

> Error Handling: The service is designed with fallbacks. If the model is down or times out, it returns a 500 status with a clear error message.

2. Grade Test
Endpoint: ```POST /grade_test```
Purpose: Grade a student's submitted answers
Request:

```
{
  "student_id": "student_123",
  "mcq_answers": [
    {
      "question_id": "mcq_1",
      "selected_answer": "A"        // Student selected option A
    }
  ],
  "code_answers": [
    {
      "question_id": "code_1",
      "code": "return a + b;"        // Student's code submission
    }
  ],
  "text_answers": [
    {
      "question_id": "text_1", 
      "answer": "JavaScript is used for web development and making websites interactive."
    }
  ]
}
```

Response:

```
{
  "student_id": "student_123",
  "overall_score": 0.85,           // 0.0 to 1.0 (85% in this case)
  "total_points": 8,               // Points earned
  "passed": true,                  // true if score >= 0.7 (70%)
  "certificate_eligible": true,    // Same as "passed" - use for NFT minting
  "breakdown": {
    "mcq": {
      "score": 1.0,               // 100% on MCQ
      "points": 2, 
      "total": 1,
      "correct": 1
    },
    "code": {
      "score": 0.7,               // 70% on code
      "points": 3,
      "total": 1
    },
    "text": {
      "score": 0.8,               // 80% on text answers
      "points": 3,
      "total": 1  
    }
  },
  "feedback": "Great job!"         // Simple feedback message
}
```

3. Generate an MCQ Test
> Endpoint: POST /generate_mcq_test

> Purpose: Generate multiple-choice questions for a given topic and difficulty.

> Request Body (JSON):

```
{
  "difficulty": "beginner",
  "question_count": 5,
  "topic": "Python"
}
```

> Response (JSON): The test data, including the correct answers and explanations.

```
{
  "test_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "type": "mcq",
  "topic": "Python",
  "difficulty": "beginner",
  "questions": [
    {
      "id": "python_mcq_1",
      "question": "Which of the following is the correct way to create a list in Python?",
      "options": {
        "A": "my_list = []",
        "B": "my_list = {}",
        "C": "my_list = ()",
        "D": "my_list = <>"
      },
      "correct": "A",
      "points": 2,
      "explanation": "Square brackets [] are used to create lists in Python"
    },
    ...
  ]
}
```

> Important: You must store the entire questions object, including the correct answer and explanation fields, to be able to grade the student's submission later. The frontend should not receive this sensitive data (the correct answer and the explanation fields).

4. Grade an MCQ Test
> Endpoint: POST /grade_mcq_test

> Purpose: Grade a student's multiple-choice answers against the stored correct answers.

> Request Body (JSON):

```
{
  "student_id": "student-123",
  "test_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "mcq_answers": [
    {
      "question_id": "python_mcq_1",
      "selected_answer": "A"
    },
    ...
  ]
}
```

> How it Works: This service retrieves the stored test data using the test_id and performs a simple check of the student's answers against the correct ones. It's a fast, non-AI grading process.

> Response (JSON): The final score and feedback for each question.

```
{
  "student_id": "student-123",
  "test_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "test_type": "mcq",
  "overall_score": 0.8,
  "total_points": 8,
  "max_possible_points": 10,
  "passed": true,
  "certificate_eligible": true,
  "grade": "B",
  "correct_answers": 4,
  "total_questions": 5,
  "feedback": [
    {
      "question_id": "python_mcq_1",
      "correct": true,
      "explanation": "Square brackets [] are used to create lists in Python"
    },
    ...
  ]
}
```


