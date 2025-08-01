* Hashproof ML System - Backend Integration Guide

** Overview
The ML System is a simple API service that generates JavaScript tests and grades student submissions using AI. It runs as a separate service that your backend can call to handle all assessment logic.

What it does:

✅ Generates JavaScript tests (MCQ, Code, Text questions)
✅ Grades student answers automatically
✅ Returns pass/fail status for NFT minting
✅ Provides detailed feedback and scores


** API Endpoints

1. Generate Test
Endpoint: ```POST /generate_test```
Purpose: Get a test with JavaScript questions for a student
Request:

```
{
  "difficulty": "beginner",     // "beginner", "intermediate", or "advanced"
  "question_count": 5           // How many questions total
}
```

Response:
```
{
  "test_id": "uuid-string",
  "questions": {
    "mcq": [
      {
        "id": "mcq_1",
        "question": "How do you declare a variable in JavaScript?",
        "options": ["A) var x = 5", "B) variable x = 5", "C) v x = 5", "D) declare x = 5"],
        "points": 2
      }
    ],
    "code": [
      {
        "id": "code_1", 
        "question": "Write a function that adds two numbers",
        "template": "function add(a, b) {\n  // Your code here\n}",
        "points": 5
      }
    ],
    "text": [
      {
        "id": "text_1",
        "question": "Explain what JavaScript is used for.",
        "points": 3
      }
    ]
  },
  "total_points": 10
}
```

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

3. Get Sample Test (for testing)
Endpoint: ```GET /sample_test```
Purpose: Get a sample test to see the format
Response: Same as generate_test response