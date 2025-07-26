from flask import Flask, request, Response, jsonify
from src.workflow import visa_question_answering
import logging
import os

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return """
    <h1>Visa Question Answering API</h1>
    <p>This is a Flask API for answering visa-related questions.</p>
    <p>Use a POST request to <code>/ask</code> with a JSON payload like:</p>
    <pre>{"question": "Your question here", "country": "US"}</pre>
    <p>Example using curl:</p>
    <pre>curl -X POST -H "Content-Type: application/json" -d '{"question":"What are the visa requirements for the US?","country":"US"}' http://127.0.0.1:5001/ask</pre>
    """

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

    def generate():
        try:
            for chunk in visa_question_answering(question, country):
                yield chunk
        except Exception as e:
            logger.error("Error processing request: %s", e)
            yield f"Error: {str(e)}"
        finally:
            yield ""  # Signal end of stream

    try:
        return Response(
            generate(),
            mimetype='text/plain',
            headers={
                'Transfer-Encoding': 'chunked',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
        )
    except Exception as e:
        logger.error("Error in response: %s", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)