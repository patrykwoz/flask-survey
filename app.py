from flask import Flask, request, flash, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "someSecret123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
all_surveys = surveys.surveys
survey_names = list(all_surveys.keys())


@app.route('/')
def home_page():

    first_survey = survey_names[0]

    return redirect(f'/{first_survey}')

@app.route('/<survey_name>')
def survey_page(survey_name):
    current_survey = all_surveys[survey_name]


    return render_template('home.html', survey = current_survey, survey_name = survey_name, survey_names=survey_names)

@app.route('/questions/<int:question_number>')
def questions_page(question_number):
    survey_name = request.args.get('survey')

    current_survey = all_surveys[survey_name]
    question_number = int(question_number)
    completed = False


    for response in responses:
        if response['survey_name'] == survey_name:
            completed = response.get('completed', False)
    
    if question_number <= 0 or question_number > len(current_survey.questions):
        flash(f"Sorry, not a valid question...")
        return redirect(f'/questions/1?survey={survey_name}')
    if completed:
        flash(f"You have already completed survey: {survey_name}...")
        return redirect('/')

    if question_number>len(current_survey.questions):
        raise
    if len(responses)>0:
        for response in responses:
            if response['survey_name'] == survey_name:
                if 'answers' in response:
                    keys = [int(choice[0]) for choice in response['answers']]
                    if keys:
                        max_key = max(keys)
                        if question_number != max_key + 1:
                            flash(f"You have already given answer to question {question_number} survey: {survey_name}...")
                            return redirect(f'/questions/{max_key + 1}?survey={survey_name}')


    current_question = current_survey.questions[question_number-1]
    next_question = -1
    if question_number < len(current_survey.questions):
        next_question = question_number + 1

    

    return render_template('questions.html', current_survey=current_survey,
    question_number=question_number, current_question=current_question,
    next_question=next_question, survey_name=survey_name, 
    survey_names=survey_names)

@app.route('/answer', methods=['POST'])
def process_answers():
    question_number = int(request.form.get('question_number'))
    survey_name = request.form.get('survey')
    current_survey = all_surveys[survey_name]
    _response = request.form

    answers_list = [(request.form.get('question_number'), request.form.get('choice'))]
    completed = False
    if question_number >= len(current_survey.questions):
        completed = True

    new_response = {
        'survey_name': request.form.get('survey'),
        'answers': answers_list,
        'completed': completed
    }

    if not responses:
        responses.append(new_response)
    else:
        for response in responses:
            if response['survey_name'] == new_response['survey_name']:
                response['completed'] = completed
                response['answers'].extend(answers_list)
                break
        else:
            responses.append(new_response)

    next_question = -1
    if question_number < len(current_survey.questions):
        next_question = question_number + 1
    
    redirect_string = f'/questions/{next_question}?survey={survey_name}'
    if next_question < 0:
        redirect_string = f'/thankyou?survey={survey_name}'


    return redirect(redirect_string)

@app.route('/thankyou')
def thankyou_page():
    survey_name = request.args.get('survey')
    current_survey = all_surveys[survey_name]

    return render_template('thankyou.html', survey_name=survey_name, survey = current_survey,
    survey_names=survey_names)
