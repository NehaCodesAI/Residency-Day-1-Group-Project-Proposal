from flask import Flask, render_template, request, redirect, url_for
from src.workflow import visa_question_answering_batch

app = Flask(__name__)

@app.route('/')
def welcome():
    # Render the welcome page
    return render_template('welcome.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        # Get the question and country from the form
        question = request.form.get('question')
        country = request.form.get('country', 'US')  # Default to 'US' if not provided

        # Call the visa_question_answering_batch function
        answer = visa_question_answering_batch(question, country)

        # Render the answer page with the question and answer
        return render_template('answer.html', question=question, answer=answer)

    # Render the answer page with an empty form if GET request
    return render_template('answer.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)