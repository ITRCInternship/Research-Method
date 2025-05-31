import os
from flask import Flask, render_template, request, redirect, url_for, session
import json
import requests

# Base Ollama URL
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

# Initialize Flask app
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.getenv('FLASK_SECRET', 'change-me')

# Load questions
questions_path = os.getenv('QUESTIONS_JSON', 'questions.json')
with open(questions_path, 'r', encoding='utf-8') as f:
    questions = json.load(f)

def build_prompt(responses: dict) -> str:
    return f"""
شما یک پژوهشگر حرفه‌ای هستید و وظیفه دارید بر اساس پاسخ‌های زیر، یک گزارش کامل و دقیق از روش تحقیق ارائه دهید.

پاسخ‌های کاربر به سوالات طراحی تحقیق به شرح زیر است:

1. موضوع تحقیق و دلیل انتخاب آن:
{responses.get("0", "")}

2. منابع بررسی‌شده و یافته‌های کلیدی:
{responses.get("1", "")}

3. ابزارهای گردآوری داده:
{", ".join(responses.get("2", [])) if isinstance(responses.get("2", []), list) else responses.get("2", "")}

4. نوع روش تحقیق انتخاب‌شده:
{responses.get("3", "")}

5. روش تحلیل داده‌ها:
{responses.get("4", "")}

6. مدت زمان و چالش‌های احتمالی:
{responses.get("5", "")}

لطفاً با توجه به اطلاعات بالا، یک تحلیل دقیق و ساختارمند از روش تحقیق این فرد ارائه دهید. گزارش شما باید شامل بخش‌های زیر باشد:

- بیان مسئله و ضرورت تحقیق  
- نوع تحقیق و رویکرد کلی آن  
- روش گردآوری داده‌ها و دلیل انتخاب ابزارها  
- شیوه تحلیل داده‌ها و توجیه انتخاب آن  
- مدت زمان و برنامه زمانی تحقیق  
- چالش‌های پیش‌رو و پیشنهادهایی برای رفع آن‌ها  

خروجی را به زبان فارسی، رسمی، و قابل استفاده در یک پروپوزال دانشگاهی بنویسید.
"""

def call_ollama(prompt: str) -> str:
    payload = {
        "model": "qwen2.5:7b",
        "messages": [
            {"role": "system", "content": "شما یک دستیار تحقیقاتی هستید."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"]

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('question', qid=0))

@app.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if qid >= len(questions):
        return redirect(url_for('summary'))

    if request.method == 'POST':
        q = questions[qid]
        if q.get('type') == 'multiple':
            answer = request.form.getlist('answer')
        else:
            answer = request.form.get('answer', '')
        responses = session.get('responses', {})
        responses[str(qid)] = answer
        session['responses'] = responses

        direction = request.form.get('direction')
        next_q = qid + 1 if direction == 'next' else max(0, qid - 1)
        return redirect(url_for('question', qid=next_q))

    progress = int((qid / len(questions)) * 100)
    return render_template('question.html', question=questions[qid], qid=qid, total=len(questions), progress=progress)

@app.route('/summary')
def summary():
    responses = session.get('responses', {})
    prompt = build_prompt(responses)
    try:
        result = call_ollama(prompt)
    except Exception as e:
        result = f"خطا در ارتباط با مدل Qwen: {str(e)}"
    return render_template('result.html', result=result)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5003))
    debug_flag = os.getenv('FLASK_DEBUG', 'true').lower() in ('1', 'true', 'yes')
    app.run(host=host, port=port, debug=debug_flag)
