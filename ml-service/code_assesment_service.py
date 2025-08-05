"""
HashProof Code Assessment System
Handles coding questions generation and AI-powered grading
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
    question_count: int = 3
    topic: str = "JavaScript"

class CodeAnswer(BaseModel):
    question_id: str
    code: str

class GradeRequest(BaseModel):
    student_id: str
    test_id: str
    code_answers: List[CodeAnswer]

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

def safe_json_parse_code(response: str, topic: str, difficulty: str, count: int) -> List[Dict]:
    """Safely parse JSON for code questions with fallback"""
    
    print(f"🔍 Raw AI Response for code: {response[:300]}...")
    
    if "AI Error:" in response:
        print(f"❌ AI Error detected, using fallback questions")
        return _create_fallback_code(topic, difficulty, count)
    
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
                print(f"✅ Successfully parsed {len(parsed)} code questions")
                return parsed
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
    
    try:
        parsed = json.loads(response)
        if isinstance(parsed, list) and len(parsed) > 0:
            print(f"✅ Successfully parsed entire response: {len(parsed)} code questions")
            return parsed
    except json.JSONDecodeError as e:
        print(f"❌ Full response JSON parsing failed: {e}")
    
    print(f"⚠️  Falling back to hardcoded code questions")
    return _create_fallback_code(topic, difficulty, count)

async def generate_code_questions(topic: str, difficulty: str, count: int) -> List[Dict]:
    """Generate coding questions with improved prompts"""
    
    try:
        templates = {
            "Python": "def solution():\n    # Your code here\n    pass",
            "JavaScript": "function solution() {\n    // Your code here\n}",
            "Java": "public static void solution() {\n    // Your code here\n}",
            "C++": "void solution() {\n    // Your code here\n}"
        }
        
        template = templates.get(topic, templates["JavaScript"])
        
        prompt = f"""Generate {count} coding questions for {topic} programming.

Return ONLY a JSON array with this exact format:

[{{"id": "c1", "question": "Write a function that adds two numbers", "template": "{template}", "solution": "// Example solution", "points": 5, "test_cases": [{{"input": "add(2,3)", "expected": "5"}}]}}]

Requirements:
- Questions about {topic} programming
- Difficulty: {difficulty} level
- Include template code for student to fill
- Include example solution
- Include test cases to validate solution
- Points: 5-10 each based on difficulty

JSON array only, no other text:"""

        print(f"🚀 Generating {count} code questions for {topic} ({difficulty})")
        response = await ai_client.ask_ai(prompt, max_tokens=2500, temperature=0.3)
        
        questions = safe_json_parse_code(response, topic, difficulty, count)
        
        valid_questions = []
        for i, q in enumerate(questions[:count]):
            try:
                question_id = f"{topic.lower()}_code_{i+1}"
                points = 5 if difficulty == "beginner" else 7 if difficulty == "intermediate" else 10
                
                valid_q = {
                    "id": question_id,
                    "question": q.get("question", f"Write a {topic} function"),
                    "template": q.get("template", template),
                    "solution": q.get("solution", "// Solution code here"),
                    "points": q.get("points", points),
                    "test_cases": q.get("test_cases", [{"input": "example", "expected": "result"}])
                }
                valid_questions.append(valid_q)
                print(f"✅ Created valid code question: {question_id}")
                
            except Exception as e:
                print(f"❌ Error processing code question {i+1}: {e}")
                continue
                
        if not valid_questions:
            print("⚠️  No valid code questions generated, using fallbacks")
            return _create_fallback_code(topic, difficulty, count)
            
        print(f"✅ Generated {len(valid_questions)} valid code questions")
        return valid_questions
        
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return _create_fallback_code(topic, difficulty, count)

def _create_fallback_code(topic: str, difficulty: str, count: int) -> List[Dict]:
    """Create reliable fallback coding questions"""
    templates = {
        "Python": "def function_name(params):\n    # Your code here\n    pass",
        "JavaScript": "function functionName(params) {\n    // Your code here\n}"
    }
    
    fallback_questions = {
        "Python": [
            {
                "question": "Write a function that takes two numbers and returns their sum",
                "template": "def add_numbers(a, b):\n    # Your code here\n    pass",
                "solution": "def add_numbers(a, b):\n    return a + b",
                "test_cases": [
                    {"input": "add_numbers(2, 3)", "expected": "5"},
                    {"input": "add_numbers(-1, 1)", "expected": "0"}
                ]
            },
            {
                "question": "Write a function that checks if a number is even",
                "template": "def is_even(number):\n    # Your code here\n    pass",
                "solution": "def is_even(number):\n    return number % 2 == 0",
                "test_cases": [
                    {"input": "is_even(4)", "expected": "True"},
                    {"input": "is_even(7)", "expected": "False"}
                ]
            },
            {
                "question": "Write a function that finds the maximum number in a list",
                "template": "def find_max(numbers):\n    # Your code here\n    pass",
                "solution": "def find_max(numbers):\n    return max(numbers)",
                "test_cases": [
                    {"input": "find_max([1, 5, 3, 9, 2])", "expected": "9"},
                    {"input": "find_max([-1, -5, -2])", "expected": "-1"}
                ]
            }
        ],
        "JavaScript": [
            {
                "question": "Write a function that greets a person by name",
                "template": "function greet(name) {\n    // Your code here\n}",
                "solution": "function greet(name) {\n    return 'Hello, ' + name + '!';\n}",
                "test_cases": [
                    {"input": "greet('Alice')", "expected": "'Hello, Alice!'"},
                    {"input": "greet('Bob')", "expected": "'Hello, Bob!'"}
                ]
            },
            {
                "question": "Write a function that doubles a number",
                "template": "function double(num) {\n    // Your code here\n}",
                "solution": "function double(num) {\n    return num * 2;\n}",
                "test_cases": [
                    {"input": "double(5)", "expected": "10"},
                    {"input": "double(-3)", "expected": "-6"}
                ]
            },
            {
                "question": "Write a function that filters even numbers from an array",
                "template": "function filterEvens(numbers) {\n    // Your code here\n}",
                "solution": "function filterEvens(numbers) {\n    return numbers.filter(num => num % 2 === 0);\n}",
                "test_cases": [
                    {"input": "filterEvens([1, 2, 3, 4, 5, 6])", "expected": "[2, 4, 6]"},
                    {"input": "filterEvens([1, 3, 5])", "expected": "[]"}
                ]
            }
        ]
    }
    
    questions = fallback_questions.get(topic, fallback_questions["JavaScript"])
    points = 5 if difficulty == "beginner" else 7 if difficulty == "intermediate" else 10
    
    result = []
    for i in range(count):
        q = questions[i % len(questions)]
        result.append({
            "id": f"{topic.lower()}_code_{i+1}",
            "question": q["question"], 
            "template": q["template"],
            "solution": q["solution"],
            "points": points,
            "test_cases": q["test_cases"]
        })
    
    return result

async def grade_code(answers: List[CodeAnswer], test_questions: List[Dict]) -> Dict:
    """Grade code questions using AI with comprehensive error handling"""
    if not answers:
        return {"score": 0, "points": 0, "total": 0, "feedback": []}
    
    total_points = 0
    feedback = []
    question_lookup = {q["id"]: q for q in test_questions}
    
    print(f"🔍 Grading {len(answers)} code answers...")
    
    for answer in answers:
        question = question_lookup.get(answer.question_id)
        if not question:
            print(f"⚠️  Question {answer.question_id} not found")
            continue
            
        try:
            print(f"🔍 Grading code for question: {answer.question_id}")
            
            prompt = f"""Grade this coding solution from 0-10:

Question: {question['question']}
Expected solution approach: {question.get('solution', 'Not provided')}
Student submitted code:
{answer.code}

Evaluate based on:
1. Correctness of logic (40%)
2. Code quality and style (30%) 
3. Completeness (30%)

Respond with: SCORE: X/10
Then provide brief feedback explaining the score."""
            
            ai_response = await asyncio.wait_for(
                ai_client.ask_ai(prompt, max_tokens=400),
                timeout=30.0
            )
            
            print(f"🔍 AI grading response: {ai_response[:200]}...")
            
            score = 5.0  # Default middle score
            if "SCORE:" in ai_response.upper():
                try:
                    lines = ai_response.split('\n')
                    score_line = next((line for line in lines if 'SCORE:' in line.upper()), None)
                    
                    if score_line:
                        score_text = score_line.split(':')[1].strip()
                        # Handle formats like "8/10", "8", "8.5/10"
                        if '/' in score_text:
                            score = float(score_text.split('/')[0])
                        else:
                            score = float(score_text.split()[0])
                        
                        score = min(10, max(0, score)) 
                        print(f"✅ Extracted score: {score}/10")
                    
                except (ValueError, IndexError) as e:
                    print(f"⚠️  Could not parse score, using default: {e}")
                    score = 5.0
            else:
                print("⚠️  No score found in AI response, using default")
                score = 5.0
            
            points_earned = int((score / 10) * question["points"])
            total_points += points_earned
            
            feedback.append({
                "question_id": answer.question_id,
                "score": f"{score}/10",
                "points_earned": points_earned,
                "max_points": question["points"],
                "feedback": ai_response if not ai_response.startswith("AI Error:") else "Code submitted successfully but could not be fully evaluated"
            })
            
            print(f"✅ Graded {answer.question_id}: {score}/10 ({points_earned}/{question['points']} points)")
            
        except asyncio.TimeoutError:
            print(f"⏰ Code grading timed out for question {answer.question_id}")
            points_earned = question["points"] // 2
            total_points += points_earned
            
            feedback.append({
                "question_id": answer.question_id,
                "score": "5/10",
                "points_earned": points_earned,
                "max_points": question["points"],
                "feedback": "Code submitted but grading timed out - partial credit given"
            })
            
        except Exception as e:
            print(f"❌ Code grading failed for question {answer.question_id}: {e}")
            points_earned = question["points"] // 2
            total_points += points_earned
            
            feedback.append({
                "question_id": answer.question_id,
                "score": "5/10",
                "points_earned": points_earned,
                "max_points": question["points"],
                "feedback": "Code submitted but could not be fully evaluated - partial credit given"
            })
    
    # Calculate overall metrics
    total_possible = sum(q["points"] for q in test_questions if q["id"] in [a.question_id for a in answers])
    avg_score = (total_points / total_possible) if total_possible > 0 else 0
    
    print(f"✅ Code grading complete: {total_points}/{total_possible} points ({avg_score:.2%})")
    
    return {
        "score": avg_score,
        "points": total_points,
        "total": len(answers),
        "feedback": feedback
    }

# TEST GENERATION AND GRADING
async def generate_code_test(topic: str, difficulty: str, count: int) -> Dict:
    """Generate a coding test"""
    test_id = str(uuid.uuid4())
    
    print(f"🚀 Generating code test: {topic} ({difficulty}) - {count} questions")
    
    try:
        code_questions = await asyncio.wait_for(
            generate_code_questions(topic, difficulty, count), 
            timeout=90.0  # Longer timeout for code generation
        )
        
        total_points = sum(q["points"] for q in code_questions)
        
        result = {
            "test_id": test_id,
            "type": "code",
            "topic": topic,
            "difficulty": difficulty,
            "questions": code_questions,
            "total_points": total_points,
            "question_count": len(code_questions)
        }
        
        print(f"✅ Code test generated: {len(code_questions)} questions, {total_points} points")
        return result
        
    except asyncio.TimeoutError:
        print("⏰ Code generation timed out, using fallbacks")
        code_questions = _create_fallback_code(topic, difficulty, count)
        total_points = sum(q["points"] for q in code_questions)
        
        return {
            "test_id": test_id,
            "type": "code",
            "topic": topic,
            "difficulty": difficulty,
            "questions": code_questions,
            "total_points": total_points,
            "question_count": len(code_questions),
            "fallback_used": True
        }
        
    except Exception as e:
        print(f"❌ Code test generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate code test: {str(e)}")

async def grade_code_test(request: GradeRequest, test_data: Dict) -> Dict:
    """Grade a coding test"""
    try:
        code_result = await grade_code(request.code_answers, test_data["questions"])
        
        overall_score = code_result["score"]
        passed = overall_score >= 0.7
        
        return {
            "student_id": request.student_id,
            "test_id": request.test_id,
            "test_type": "code",
            "overall_score": round(overall_score, 2),
            "total_points": code_result["points"],
            "max_possible_points": test_data["total_points"],
            "passed": passed,
            "certificate_eligible": passed,
            "grade": "A" if overall_score >= 0.9 else "B" if overall_score >= 0.8 else "C" if overall_score >= 0.7 else "D" if overall_score >= 0.6 else "F",
            "questions_graded": code_result["total"],
            "feedback": code_result["feedback"],
            "message": "Excellent coding skills!" if overall_score >= 0.9 else "Good programming work!" if passed else "Keep practicing your coding skills!"
        }
        
    except Exception as e:
        print(f"❌ Code grading failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to grade code test: {str(e)}")

# STORAGE
TEST_STORAGE = {}

# FASTAPI APP
app = FastAPI(
    title="HashProof Code Assessment System", 
    description="AI-powered coding assessment system using DeepSeek",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "HashProof Code Assessment System is running!", 
        "status": "healthy",
        "ai_model": MODEL,
        "type": "Code Assessment",
        "features": ["AI-generated coding questions", "Intelligent code grading", "Multiple programming languages"]
    }

@app.post("/generate_code_test")
async def create_code_test(request: TestRequest):
    """Generate a coding test"""
    try:
        if request.question_count < 1 or request.question_count > 10:
            raise HTTPException(status_code=400, detail="Question count must be between 1 and 10 for coding tests")
        
        if request.difficulty not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(status_code=400, detail="Difficulty must be beginner, intermediate, or advanced")
        
        result = await generate_code_test(request.topic, request.difficulty, request.question_count)
        TEST_STORAGE[result["test_id"]] = result
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate code test: {str(e)}")

@app.post("/grade_code_test")
async def grade_code_assessment(request: GradeRequest):
    """Grade a coding test"""
    try:
        test_data = TEST_STORAGE.get(request.test_id)
        if not test_data:
            raise HTTPException(status_code=404, detail="Test not found. Please generate a test first.")
        
        if not request.code_answers:
            raise HTTPException(status_code=400, detail="No code answers provided")
            
        result = await grade_code_test(request, test_data)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to grade code test: {str(e)}")

@app.get("/sample_code_test")
async def get_sample_code():
    """Get a sample coding test"""
    try:
        sample_request = TestRequest(difficulty="beginner", question_count=3, topic="JavaScript")
        result = await generate_code_test(sample_request.topic, sample_request.difficulty, sample_request.question_count)
        TEST_STORAGE[result["test_id"]] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sample code test: {str(e)}")

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
            "type": "Code Assessment System"
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