from flask import Flask, render_template, request, jsonify
from src.workflow import visa_question_answering_batch
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/chat')
def chat():
    country = request.args.get('country', 'US')
    return render_template('chatbot.html', country=country)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    country = data.get('country', 'US')  # Default to US if not provided
    logging.info(f"Received question: {question} for country: {country}")
    
    try:
        answer = visa_question_answering_batch(question, country)
        return jsonify({'answer': answer})
    except Exception as e:
        logging.error(f"Error processing question: {e}")
        return jsonify({'answer': 'Oops! Something went wrong. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)