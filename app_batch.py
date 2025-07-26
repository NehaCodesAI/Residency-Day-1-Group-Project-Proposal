from flask import Flask, request, Response, jsonify
from src.workflow import visa_question_answering

app = Flask(__name__)


@app.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint to handle visa-related questions.
    """
    data = request.json
    question = data.get('question')
    country = data.get('country', 'US')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Stream the response using Flask's Response object
    return Response(visa_question_answering(question, country), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)