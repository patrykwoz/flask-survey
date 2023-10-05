from flask import Flask, request, flash, render_template, redirect
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


    return render_template('home.html', survey = current_survey, survey_names = survey_names)