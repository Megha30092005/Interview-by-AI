import json
from services.llm_service import generate

def generate_mcqs(topic="aptitude"):
    prompt = f"""
Generate exactly 10 multiple choice questions.

Topic:
{topic}

Rules:
- Each question must have 4 options
- One correct answer
- The correct answer must appear in the options
- Return ONLY valid JSON
- Do not include explanations

JSON format:

[
  {{
    "question": "What is Python?",
    "options": ["Programming language","Database","Operating system","Browser"],
    "answer": "Programming language"
  }}
]
"""

    response = generate(prompt)

    def extract_json(text):
        start = text.find("[")
        end = text.rfind("]") + 1
        return text[start:end]

    try:
        clean = extract_json(response)
        questions = json.loads(clean)

        if isinstance(questions, list) and len(questions) >= 5:
            return questions[:10]

    except:
        pass

    # fallback
    return [
        {"question": "2 + 2 = ?", "options": ["1","2","3","4"], "answer": "4"},
        {"question": "5 * 3 = ?", "options": ["15","10","20","25"], "answer": "15"},
        {"question": "10 / 2 = ?", "options": ["2","5","10","20"], "answer": "5"},
        {"question": "3 + 6 = ?", "options": ["7","8","9","10"], "answer": "9"},
        {"question": "7 - 2 = ?", "options": ["3","4","5","6"], "answer": "5"}
    ]