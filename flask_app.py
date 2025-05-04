from flask import Flask, render_template, request, redirect
from HelpRequest import get_pending_requests, get_resolved_requests, update_help_request

app = Flask(__name__)

router = None  # Will be set by main.py

@app.route('/')
def index():
    pending = get_pending_requests()
    resolved = get_resolved_requests()
    return render_template('index.html', pending=pending, resolved=resolved)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    req_id = request.form['req_id']
    answer = request.form['answer']
    update_help_request(req_id, answer)
    if router:
        router.submit_employee_answer(req_id, answer)
    return redirect('/')
