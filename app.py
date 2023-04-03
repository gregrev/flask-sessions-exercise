from flask import Flask, request, render_template, redirect, flash, jsonify, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# variable for the session
RESPONSES = "responses"

# create root route and get the data from surveys.py
@app.route('/')
def start_page():
    """displat start page"""
    return render_template("startpage.html", survey=satisfaction_survey)

# create route to handle start of survey
@app.route("/start", methods=["POST"])
def start():
    # each time start the survey clear responses from list
    session[RESPONSES] = []
    # and direct to the first question
    return redirect('/questions/0')

# routw that handles the answer to the questions
@app.route('/answer', methods=["POST"])
def submit_ans():
    """save answer and add to list and redirect to next question"""

    # grab response
    ans = request.form['input']
    # grab response list of current session
    responses = session[RESPONSES]
    # add response to session list
    responses.append(ans)
    # rebind save updated list to session
    session[RESPONSES] = responses
    
    # if the length of answers and number of survey questions are equal user is complete with survey direct to complete page
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    # if not compelte redirect to the next question
    else:
        return redirect(f"/questions/{len(responses)}")
    # raise

# route to display the questions
@app.route('/questions/<int:qid>')
def questions(qid):
    # grab the current session list of responses
    responses = session.get(RESPONSES)
    # if there is no responses direct to the start page
    if (responses is None):
        return redirect("/")
    # if user answered all the questions send to start page
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    # if questioun number is not in responses flash error
    if (len(responses) != qid):
        flash(f"Question id:({qid}) is not valid.")
        return redirect(f"/questions/{len(responses)}")

    # grab current question from data and render queastion page
    question = satisfaction_survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

# route to show survey is complete
@app.route("/complete")
def complete():
    """Survey complete"""
    return render_template("complete.html")