from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, g
from .llm.vllm_server import Llm
from .llm.prompts import research_method_prompt, system_prompt
import markdown2


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

    all_questions = current_app.questions
    responses = session.get('responses', {})

    selected_approach = responses.get('8')

    def should_include(q):
        cond = q.get('condition')
        if not cond:
            return True
        if selected_approach == 'آمیخته':
            return cond in ['کمی', 'کیفی']
        return cond == selected_approach

    filtered_questions = [q for q in all_questions if should_include(q)]
    total = len(filtered_questions)

    if qid >= total:
        return redirect(url_for('main.summary'))

    question = filtered_questions[qid]
    print(question)

    if request.method == 'POST':
        if question.get('type') == 'variables_table':
            variables_data = request.form.get('variablesData', '[]')
            responses[str(question['id'])] = variables_data
        elif question.get('type') == 'multiple':
            answer = request.form.getlist('answer')
            responses[str(question['id'])] = answer
        else:
            answer = request.form.get('answer', '')
            responses[str(question['id'])] = answer

        session['responses'] = responses

        direction = request.form.get('direction')
        next_q = qid + 1 if direction == 'next' else max(0, qid - 1)

        return redirect(url_for('main.question', qid=next_q))

    progress = int((qid / total) * 100)

    return render_template(
        'question.html',
        question=question,
        qid=qid,
        total=total,
        progress=progress
    )



@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/summary')
def summary():
    if g.user is None:
        return redirect(url_for('auth.login'))

    all_questions = current_app.questions
    responses = session.get('responses', {})

    questions_with_answers = []
    for q in all_questions:
        answer = responses.get(str(q['id']), None)
        questions_with_answers.append({
            'question': q['text'],
            'answer': answer
        })

    return render_template('summary.html', qa_list=questions_with_answers)





@main_bp.route('/result')
def result():
    questions = current_app.questions
    responses = session.get('responses', {})

    combined_text = ""
    for q in questions:
        answer = responses.get(str(q['id']), '')
        combined_text += f"سؤال: {q['text']}\nپاسخ: {answer}\n\n"

    user_prompt = research_method_prompt(combined_text)
    llm = Llm()
    response = llm.vllm_inference(user_message=user_prompt, system_message=system_prompt)

    llm_answer = None
    if response and 'choices' in response:
        llm_answer = (response['choices'][0]['message']['content'])
    llm_answer = markdown2.markdown(llm_answer)
    return render_template('result.html', llm_answer=llm_answer)