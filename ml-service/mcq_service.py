"""
HashProof MCQ Assessment System
Handles Multiple Choice Questions generation and grading
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
from openai import OpenAI
import json
import uuid
import asyncio
import os
from dotenv import load_dotenv

load_dotenv() 

# CONFIGURATION
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://router.huggingface.co/v1"
MODEL = "deepseek-ai/DeepSeek-R1:novita"

# DATA MODELS
class TestRequest(BaseModel):
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    question_count: int = 5
    topic: str = "JavaScript"

class MCQAnswer(BaseModel):
    question_id: str
    selected_answer: str  # A, B, C, or D

class GradeRequest(BaseModel):
    student_id: str
    test_id: str
    mcq_answers: List[MCQAnswer]

class DeepSeekClient:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            print("⚠️  Warning: DEEPSEEK_API_KEY environment variable not set!")
            self.client = None
        else:
            self.client = OpenAI(
                base_url=DEEPSEEK_BASE_URL,
                api_key=DEEPSEEK_API_KEY,
                timeout=120.0
            )

    async def ask_ai(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.3) -> str:
        """Ask DeepSeek AI via HuggingFace with the official openai library"""
        if not self.client:
            return "AI Error: DEEPSEEK_API_KEY not set."

        print(f"🔍 Making API request to: {DEEPSEEK_BASE_URL} with model {MODEL}")

        try:
            completion = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response_text = completion.choices[0].message.content
            return response_text

        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"❌ {error_msg}")
            return f"AI Error: {error_msg}"

ai_client = DeepSeekClient()

def safe_json_parse(response: str, topic: str, difficulty: str, count: int) -> List[Dict]:
    """Safely parse JSON with comprehensive error handling"""
    
    print(f"🔍 Raw AI Response: {response[:300]}...")
    
    # Check if response contains an error
    if "AI Error:" in response:
        print(f"❌ AI Error detected, using fallback questions")
        return _create_fallback_mcq(topic, difficulty, count)
    
    response = response.strip()
    
    if response.startswith('```json'):
        response = response[7:]
    if response.startswith('```'):
        response = response[3:]
    if response.endswith('```'):
        response = response[:-3]
    response = response.strip()
    
    json_start = response.find('[')
    json_end = response.rfind(']') + 1
    
    if json_start != -1 and json_end > json_start:
        json_str = response[json_start:json_end]
        print(f"🔍 Extracted JSON: {json_str[:200]}...")
        
        try:
            parsed = json.loads(json_str)
            if isinstance(parsed, list) and len(parsed) > 0:
                print(f"✅ Successfully parsed {len(parsed)} questions")
                return parsed
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
    
    try:
        parsed = json.loads(response)
        if isinstance(parsed, list) and len(parsed) > 0:
            print(f"✅ Successfully parsed entire response: {len(parsed)} questions")
            return parsed
    except json.JSONDecodeError as e:
        print(f"❌ Full response JSON parsing failed: {e}")
    
    print(f"⚠️  Falling back to hardcoded questions")
    return _create_fallback_mcq(topic, difficulty, count)

# MCQ QUESTION GENERATION
async def generate_mcq_questions(topic: str, difficulty: str, count: int) -> List[Dict]:
    """Generate MCQ questions with improved prompts"""
    
    try:
        prompt = f"""Generate {count} multiple choice questions about {topic} programming.

Return ONLY a JSON array with this exact format:

[{{"id": "q1", "question": "What is a variable in {topic}?", "options": {{"A": "Stores data", "B": "Wrong answer", "C": "Also wrong", "D": "Wrong too"}}, "correct": "A", "points": 2, "explanation": "Variables store data values"}}]

Requirements:
- Questions about {topic} programming
- Difficulty: {difficulty} level
- Each question worth 2-4 points based on difficulty
- Options must use A, B, C, D format
- Include brief explanations

JSON array only, no other text:"""

        print(f"🚀 Generating {count} MCQ questions for {topic} ({difficulty})")
        response = await ai_client.ask_ai(prompt, max_tokens=2000, temperature=0.3)
        
        questions = safe_json_parse(response, topic, difficulty, count)
        
        # Validate and fix each question
        valid_questions = []
        for i, q in enumerate(questions[:count]):
            try:
                question_id = f"{topic.lower()}_mcq_{i+1}"
                points = q.get("points", 2 if difficulty == "beginner" else 3 if difficulty == "intermediate" else 4)
                
                options = q.get("options", {})
                if isinstance(options, list):
                    # Convert list to dict
                    option_dict = {}
                    letters = ["A", "B", "C", "D"]
                    for idx, opt in enumerate(options[:4]):
                        clean_opt = opt.split(") ", 1)[-1] if ") " in opt else opt
                        option_dict[letters[idx]] = clean_opt
                    options = option_dict
                
                required_keys = ["A", "B", "C", "D"]
                if not all(key in options for key in required_keys):
                    print(f"⚠️  Question {i+1} missing required options, skipping")
                    continue
                    
                valid_q = {
                    "id": question_id,
                    "question": q.get("question", f"What is an important concept in {topic}?"),
                    "options": options,
                    "correct": q.get("correct", "A") if q.get("correct") in required_keys else "A",
                    "points": points,
                    "explanation": q.get("explanation", "Check the documentation for details")
                }
                valid_questions.append(valid_q)
                print(f"✅ Created valid MCQ question: {question_id}")
                
            except Exception as e:
                print(f"❌ Error processing MCQ question {i+1}: {e}")
                continue
                
        if not valid_questions:
            print("⚠️  No valid questions generated, using fallbacks")
            return _create_fallback_mcq(topic, difficulty, count)
            
        print(f"✅ Generated {len(valid_questions)} valid MCQ questions")
        return valid_questions
        
    except Exception as e:
        print(f"❌ MCQ generation failed: {e}")
        return _create_fallback_mcq(topic, difficulty, count)

def _create_fallback_mcq(topic: str, difficulty: str, count: int) -> List[Dict]:
    """Create reliable fallback MCQ questions"""
    fallback_questions = {
        "Python": [
            {
                "question": "Which of the following is the correct way to create a list in Python?",
                "options": {
                    "A": "my_list = []",
                    "B": "my_list = {}",
                    "C": "my_list = ()",
                    "D": "my_list = <>"
                },
                "correct": "A",
                "explanation": "Square brackets [] are used to create lists in Python"
            },
            {
                "question": "What is the output of print(type(5.0)) in Python?",
                "options": {
                    "A": "<class 'int'>",
                    "B": "<class 'float'>", 
                    "C": "<class 'number'>",
                    "D": "<class 'double'>"
                },
                "correct": "B", 
                "explanation": "5.0 is a floating-point number, so type() returns <class 'float'>"
            },
            {
                "question": "How do you create a comment in Python?",
                "options": {
                    "A": "// This is a comment",
                    "B": "/* This is a comment */",
                    "C": "# This is a comment", 
                    "D": "<!-- This is a comment -->"
                },
                "correct": "C",
                "explanation": "Python uses # for single-line comments"
            },
            {
                "question": "What is the correct way to define a function in Python?",
                "options": {
                    "A": "def function_name():",
                    "B": "function function_name():",
                    "C": "define function_name():",
                    "D": "func function_name():"
                },
                "correct": "A",
                "explanation": "Python uses 'def' keyword to define functions"
            }
        ],
        "JavaScript": [
            {
                "question": "How do you declare a variable in JavaScript?",
                "options": {
                    "A": "var x = 5",
                    "B": "variable x = 5",
                    "C": "v x = 5",
                    "D": "declare x = 5"
                },
                "correct": "A",
                "explanation": "The 'var' keyword is used to declare variables in JavaScript"
            },
            {
                "question": "What does the === operator do in JavaScript?",
                "options": {
                    "A": "Assigns a value",
                    "B": "Compares value only",
                    "C": "Compares value and type",
                    "D": "Creates a variable"
                },
                "correct": "C",
                "explanation": "The === operator performs strict equality comparison, checking both value and type"
            },
            {
                "question": "Which method adds an element to the end of an array?",
                "options": {
                    "A": "push()",
                    "B": "add()",
                    "C": "append()",
                    "D": "insert()"
                },
                "correct": "A",
                "explanation": "The push() method adds elements to the end of an array"
            },
            {
                "question": "How do you create a function in JavaScript?",
                "options": {
                    "A": "function myFunction() {}",
                    "B": "def myFunction() {}",
                    "C": "create myFunction() {}",
                    "D": "func myFunction() {}"
                },
                "correct": "A",
                "explanation": "JavaScript uses 'function' keyword to create functions"
            }
        ]
    }
    
    questions = fallback_questions.get(topic, fallback_questions["JavaScript"])
    points = 2 if difficulty == "beginner" else 3 if difficulty == "intermediate" else 4
    
    result = []
    for i in range(count):
        q = questions[i % len(questions)] 
        result.append({
            "id": f"{topic.lower()}_mcq_{i+1}",
            "question": q["question"],
            "options": q["options"],
            "correct": q["correct"],
            "points": points,
            "explanation": q["explanation"]
        })
    
    return result

# MCQ GRADING
async def grade_mcq(answers: List[MCQAnswer], test_questions: List[Dict]) -> Dict:
    """Grade multiple choice questions"""
    if not answers:
        return {"score": 0, "points": 0, "total": 0, "feedback": []}
    
    correct = 0
    total_points = 0
    feedback = []
    
    question_lookup = {q["id"]: q for q in test_questions}
    
    for answer in answers:
        question = question_lookup.get(answer.question_id)
        
        if question:
            if answer.selected_answer == question["correct"]:
                correct += 1
                total_points += question["points"]
                feedback.append({
                    "question_id": answer.question_id,
                    "correct": True,
                    "explanation": question.get("explanation", "Correct!")
                })
            else:
                feedback.append({
                    "question_id": answer.question_id,
                    "correct": False,
                    "explanation": question.get("explanation", f"Correct answer was {question['correct']}")
                })
    
    return {
        "score": correct / len(answers) if answers else 0,
        "points": total_points,
        "total": len(answers),
        "correct": correct,
        "feedback": feedback
    }

# TEST GENERATION AND GRADING
async def generate_mcq_test(topic: str, difficulty: str, count: int) -> Dict:
    """Generate an MCQ test"""
    test_id = str(uuid.uuid4())
    
    print(f"🚀 Generating MCQ test: {topic} ({difficulty}) - {count} questions")
    
    try:
        mcq_questions = await asyncio.wait_for(
            generate_mcq_questions(topic, difficulty, count), 
            timeout=60.0
        )
        
        total_points = sum(q["points"] for q in mcq_questions)
        
        result = {
            "test_id": test_id,
            "type": "mcq",
            "topic": topic,
            "difficulty": difficulty,
            "questions": mcq_questions,
            "total_points": total_points,
            "question_count": len(mcq_questions)
        }
        
        print(f"✅ MCQ test generated: {len(mcq_questions)} questions, {total_points} points")
        return result
        
    except asyncio.TimeoutError:
        print("⏰ MCQ generation timed out, using fallbacks")
        mcq_questions = _create_fallback_mcq(topic, difficulty, count)
        total_points = sum(q["points"] for q in mcq_questions)
        
        return {
            "test_id": test_id,
            "type": "mcq",
            "topic": topic,
            "difficulty": difficulty,
            "questions": mcq_questions,
            "total_points": total_points,
            "question_count": len(mcq_questions),
            "fallback_used": True
        }
    except Exception as e:
        print(f"❌ MCQ test generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate MCQ test: {str(e)}")

async def grade_mcq_test(request: GradeRequest, test_data: Dict) -> Dict:
    """Grade an MCQ test"""
    try:
        mcq_result = await grade_mcq(request.mcq_answers, test_data["questions"])
        
        overall_score = mcq_result["score"]
        passed = overall_score >= 0.7
        
        return {
            "student_id": request.student_id,
            "test_id": request.test_id,
            "test_type": "mcq",
            "overall_score": round(overall_score, 2),
            "total_points": mcq_result["points"],
            "max_possible_points": test_data["total_points"],
            "passed": passed,
            "certificate_eligible": passed,
            "grade": "A" if overall_score >= 0.9 else "B" if overall_score >= 0.8 else "C" if overall_score >= 0.7 else "D" if overall_score >= 0.6 else "F",
            "correct_answers": mcq_result["correct"],
            "total_questions": mcq_result["total"],
            "feedback": mcq_result["feedback"],
            "message": "Excellent work!" if overall_score >= 0.9 else "Good job!" if passed else "Keep practicing and try again!"
        }
        
    except Exception as e:
        print(f"❌ MCQ grading failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to grade MCQ test: {str(e)}")

# STORAGE
TEST_STORAGE = {}

# FASTAPI APP
app = FastAPI(
    title="HashProof MCQ Assessment System", 
    description="AI-powered MCQ assessment system using DeepSeek",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "HashProof MCQ Assessment System is running!", 
        "status": "healthy",
        "ai_model": MODEL,
        "type": "MCQ Assessment",
        "features": ["AI-generated MCQ questions", "Intelligent MCQ grading", "Multiple topics and difficulties"]
    }

@app.post("/generate_mcq_test")
async def create_mcq_test(request: TestRequest):
    """Generate an MCQ test"""
    try:
        if request.question_count < 1 or request.question_count > 20:
            raise HTTPException(status_code=400, detail="Question count must be between 1 and 20")
        
        if request.difficulty not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(status_code=400, detail="Difficulty must be beginner, intermediate, or advanced")
        
        result = await generate_mcq_test(request.topic, request.difficulty, request.question_count)
        TEST_STORAGE[result["test_id"]] = result
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate MCQ test: {str(e)}")

@app.post("/grade_mcq_test")
async def grade_mcq_assessment(request: GradeRequest):
    """Grade an MCQ test"""
    try:
        test_data = TEST_STORAGE.get(request.test_id)
        if not test_data:
            raise HTTPException(status_code=404, detail="Test not found. Please generate a test first.")
        
        if not request.mcq_answers:
            raise HTTPException(status_code=400, detail="No MCQ answers provided")
            
        result = await grade_mcq_test(request, test_data)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to grade MCQ test: {str(e)}")

@app.get("/sample_mcq_test")
async def get_sample_mcq():
    """Get a sample MCQ test"""
    try:
        sample_request = TestRequest(difficulty="beginner", question_count=5, topic="JavaScript")
        result = await generate_mcq_test(sample_request.topic, sample_request.difficulty, sample_request.question_count)
        TEST_STORAGE[result["test_id"]] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sample MCQ test: {str(e)}")

@app.get("/test/{test_id}")
async def get_test(test_id: str):
    """Retrieve a test by ID"""
    test_data = TEST_STORAGE.get(test_id)
    if not test_data:
        raise HTTPException(status_code=404, detail="Test not found")
    return test_data

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        test_response = await ai_client.ask_ai("Say 'OK' if you can respond", max_tokens=10)
        ai_healthy = "OK" in test_response or "ok" in test_response.lower()
        
        return {
            "status": "healthy" if ai_healthy else "degraded",
            "ai_connection": "connected" if ai_healthy else "issues",
            "model": MODEL,
            "tests_in_memory": len(TEST_STORAGE),
            "type": "MCQ Assessment System"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "ai_connection": "failed"
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
