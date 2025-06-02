from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, g
from .ollama_client import build_prompt, call_ollama

main_bp = Blueprint('main', __name__)

@main_bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # Get database connection and load user from database
        db = current_app.extensions.get('db') or None
        if db is None:
            from . import get_db
            db = get_db()
        user = db.execute('SELECT id, username FROM user WHERE id = ?', (user_id,)).fetchone()
        g.user = user

@main_bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    session.pop('responses', None)
    return redirect(url_for('main.question', qid=0))

@main_bp.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if g.user is None:
        return redirect(url_for('auth.login'))
    questions = current_app.questions
    total = len(questions)
    if qid >= total:
        return redirect(url_for('main.summary'))
    if request.method == 'POST':
        q = questions[qid]
        # Handle multiple-choice vs text answers
        if q.get('type') == 'multiple':
            answer = request.form.getlist('answer')
        else:
            answer = request.form.get('answer', '')
        responses = session.get('responses', {})
        responses[str(qid)] = answer
        session['responses'] = responses
        # Determine navigation direction
        direction = request.form.get('direction')
        next_q = qid + 1 if direction == 'next' else max(0, qid - 1)
        return redirect(url_for('main.question', qid=next_q))
    progress = int((qid / total) * 100)
    question = questions[qid]
    return render_template('question.html', question=question, qid=qid, total=total, progress=progress)

@main_bp.route('/summary')
def summary():
    if g.user is None:
        return redirect(url_for('auth.login'))
    responses = session.get('responses', {})
    prompt = build_prompt(responses)
    try:
        result = call_ollama(prompt)
    except Exception as e:
        result = f"Error communicating with Qwen model: {str(e)}"
    return render_template('result.html', result=result)