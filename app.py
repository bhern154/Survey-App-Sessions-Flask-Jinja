from flask import Flask, request, render_template, redirect, flash
from flask import session, make_response
from surveys import satisfaction_survey

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECRET_KEY'] = "4sdlkspdfkps#$RGR^HDG"

@app.route('/')
def start_survey():
    """Shows the user the title of the survey, the instructions, and a button to start the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    questions = satisfaction_survey.questions
    
    return render_template("survey_intro.html", title=title, instructions=instructions, questions=questions)

@app.route('/set-session')
def set_session():

    session['responses'] = []

    return redirect("/questions/0")

@app.route('/questions/<int:question>')
def survey_question(question):

    print(session['responses'])

    if question != len(session['responses']):
        flash(f"Invalid question - please proceed with the survey :)")
        return redirect(f"/questions/{len(session['responses'])}")
    else:
        question_text = satisfaction_survey.questions[question].question
        choices = satisfaction_survey.questions[question].choices
        return render_template("questions.html", question_text=question_text, choices=choices)

@app.route('/answer')
def answer():

    responses = session['responses']
    responses.append(request.args["choice"])
    session['responses'] = responses

    if len(session['responses']) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/thank_you")
    
@app.route('/thank_you')
def thank_you():
    print(session['responses'])
    return render_template("thank_you.html")