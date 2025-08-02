"""
HashProof ML System

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import httpx
import json
import random
import uuid
import asyncio
import os

# CONFIGURATION

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "anthropic/claude-3-5-sonnet-20241022"

# DATA MODELS

class TestRequest(BaseModel):
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    question_count: int = 5

class MCQAnswer(BaseModel):
    question_id: str
    selected_answer: str  # A, B, C, or D

class CodeAnswer(BaseModel):
    question_id: str
    code: str

class TextAnswer(BaseModel):
    question_id: str
    answer: str

class GradeRequest(BaseModel):
    student_id: str
    mcq_answers: List[MCQAnswer] = []
    code_answers: List[CodeAnswer] = []
    text_answers: List[TextAnswer] = []


# JAVASCRIPT QUESTIONS DATABASE

QUESTIONS = {
    "beginner": {
        "mcq": [
            {
                "id": "mcq_1",
                "question": "How do you declare a variable in JavaScript?",
                "options": ["A) var x = 5", "B) variable x = 5", "C) v x = 5", "D) declare x = 5"],
                "correct": "A",
                "points": 2
            },
            {
                "id": "mcq_2", 
                "question": "What does '===' do in JavaScript?",
                "options": ["A) Assigns value", "B) Compares value only", "C) Compares value and type", "D) Nothing"],
                "correct": "C",
                "points": 2
            },
            {
                "id": "mcq_3",
                "question": "How do you write a comment in JavaScript?",
                "options": ["A) # comment", "B) // comment", "C) <!-- comment -->", "D) ** comment **"],
                "correct": "B", 
                "points": 2
            }
        ],
        "code": [
            {
                "id": "code_1",
                "question": "Write a function that adds two numbers",
                "template": "function add(a, b) {\n  // Your code here\n}",
                "solution": "return a + b;",
                "points": 5
            },
            {
                "id": "code_2",
                "question": "Write a function that returns 'Hello, [name]!'",
                "template": "function greet(name) {\n  // Your code here\n}",
                "solution": "return 'Hello, ' + name + '!';",
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
    "intermediate": {
        "mcq": [
            {
                "id": "mcq_4",
                "question": "What does 'typeof null' return?",
                "options": ["A) 'null'", "B) 'undefined'", "C) 'object'", "D) 'boolean'"],
                "correct": "C",
                "points": 3
            }
        ],
        "code": [
            {
                "id": "code_3", 
                "question": "Write a function that finds the maximum number in an array",
                "template": "function findMax(arr) {\n  // Your code here\n}",
                "solution": "return Math.max(...arr);",
                "points": 6
            }
        ],
        "text": [
            {
                "id": "text_2",
                "question": "Explain what closures are in JavaScript.",
                "points": 4
            }
        ]
    }
}


# AI CLIENT

class AIClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def ask_ai(self, prompt: str) -> str:
        """Ask AI a question and get response"""
        try:
            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    return f"AI Error: {response.status_code}"
                    
        except Exception as e:
            return f"AI Error: {str(e)}"

ai_client = AIClient()


# MAIN ML FUNCTIONS

def generate_test(difficulty: str, count: int) -> Dict:
    """Generate a test from question bank"""
    test_id = str(uuid.uuid4())
    
    questions_pool = QUESTIONS.get(difficulty, QUESTIONS["beginner"])
    
    # Pick questions
    selected = {
        "mcq": random.sample(questions_pool["mcq"], min(count//2, len(questions_pool["mcq"]))),
        "code": random.sample(questions_pool["code"], min(count//3, len(questions_pool["code"]))), 
        "text": random.sample(questions_pool["text"], min(count//5, len(questions_pool["text"])))
    }
    
    total_points = sum(
        sum(q["points"] for q in selected[qtype]) 
        for qtype in selected
    )
    
    return {
        "test_id": test_id,
        "questions": selected,
        "total_points": total_points
    }

async def grade_mcq(answers: List[MCQAnswer]) -> Dict:
    """Grade multiple choice questions"""
    if not answers:
        return {"score": 0, "points": 0, "total": 0}
    
    correct = 0
    total_points = 0
    
    for answer in answers:
        # Find the question
        question = None
        for difficulty in QUESTIONS.values():
            for mcq in difficulty["mcq"]:
                if mcq["id"] == answer.question_id:
                    question = mcq
                    break
        
        if question and answer.selected_answer == question["correct"]:
            correct += 1
            total_points += question["points"]
    
    return {
        "score": correct / len(answers) if answers else 0,
        "points": total_points,
        "total": len(answers),
        "correct": correct
    }

async def grade_code(answers: List[CodeAnswer]) -> Dict:
    """Grade code questions (simplified - just check if code exists)"""
    if not answers:
        return {"score": 0, "points": 0, "total": 0}
    
    total_points = 0
    
    for answer in answers:
        # Simple check: if code has some content, give partial points
        if answer.code.strip() and len(answer.code.strip()) > 10:
            # Find question points
            question_points = 5  # default
            for difficulty in QUESTIONS.values():
                for code_q in difficulty["code"]:
                    if code_q["id"] == answer.question_id:
                        question_points = code_q["points"]
                        break
            
            # Give 70% points if code looks reasonable
            if "return" in answer.code and len(answer.code.strip()) > 20:
                total_points += int(question_points * 0.7)
            else:
                total_points += int(question_points * 0.3)
    
    return {
        "score": 0.7 if answers else 0,  # Assume 70% for submitted code
        "points": total_points,
        "total": len(answers)
    }

async def grade_text(answers: List[TextAnswer]) -> Dict:
    """Grade text answers using AI"""
    if not answers:
        return {"score": 0, "points": 0, "total": 0}
    
    total_score = 0
    total_points = 0
    
    for answer in answers:
        # Ask AI to grade the answer
        prompt = f"""
        Grade this JavaScript answer on scale 0-10:
        Question: {answer.question_id}
        Answer: {answer.answer}
        
        Just respond with a number 0-10, nothing else.
        """
        
        ai_response = await ai_client.ask_ai(prompt)
        
        try:
            # Extract number from AI response
            score = float(''.join(c for c in ai_response if c.isdigit() or c == '.'))
            score = min(10, max(0, score))  # Clamp between 0-10
            total_score += score
            total_points += int((score / 10) * 3)  # 3 points per text question
        except:
            total_score += 5  # Default middle score
            total_points += 1
    
    avg_score = (total_score / len(answers)) / 10 if answers else 0
    
    return {
        "score": avg_score,
        "points": total_points,
        "total": len(answers)
    }

async def grade_assessment(request: GradeRequest) -> Dict:
    """Grade complete assessment"""
    
    # Grade each section
    mcq_result = await grade_mcq(request.mcq_answers)
    code_result = await grade_code(request.code_answers)
    text_result = await grade_text(request.text_answers)
    
    # Calculate overall score
    total_points = mcq_result["points"] + code_result["points"] + text_result["points"]
    max_possible = (len(request.mcq_answers) * 2) + (len(request.code_answers) * 5) + (len(request.text_answers) * 3)
    
    overall_score = total_points / max_possible if max_possible > 0 else 0
    passed = overall_score >= 0.7
    
    return {
        "student_id": request.student_id,
        "overall_score": round(overall_score, 2),
        "total_points": total_points,
        "passed": passed,
        "certificate_eligible": passed,
        "breakdown": {
            "mcq": mcq_result,
            "code": code_result, 
            "text": text_result
        },
        "feedback": "Great job!" if passed else "Keep practicing!"
    }


# FASTAPI APP

app = FastAPI(title="HashProof ML System")

@app.get("/")
async def root():
    return {"message": "HashProof ML System is running!", "status": "healthy"}

@app.post("/generate_test")
async def create_test(request: TestRequest):
    """Generate a test"""
    try:
        result = generate_test(request.difficulty, request.question_count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grade_test") 
async def grade_test(request: GradeRequest):
    """Grade a test"""
    try:
        result = await grade_assessment(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample_test")
async def get_sample():
    """Get a sample test for testing"""
    return generate_test("beginner", 3)


# RUN THE SERVER

if __name__ == "__main__":
    print("🚀 Starting HashProof ML System...")
    print(f"📍 Open: http://localhost:8080")
    print(f"📋 Sample test: http://localhost:8080/sample_test")
    print(f"📖 Docs: http://localhost:8080/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")