from flask import Flask, request, jsonify, send_from_directory, session
from flask_session import Session
from datetime import timedelta

from utils.ai_model import HybridAssistant
from utils.flask_secret_key import ensure_secret_key, load_secret_key
from utils.api_handlers import extract_location, extract_topic, get_weather, get_news, get_cat_fact

ensure_secret_key()

# --- Flask App --- #
app = Flask(__name__, static_folder='static')
app.secret_key = load_secret_key()

# Session Config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)
assistant = HybridAssistant()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()  # Convert to lowercase for easier matching

    # Initialize session memory if not present
    if 'conversation' not in session:
        session['conversation'] = []

    # Append the user's message to the conversation    
    if user_message:
        session['conversation'].append({'sender': 'user', 'message': user_message})

    bot_reply = assistant.generate_response(user_message)

    # Store conversation    
    session['conversation'].append({'sender': 'bot', 'message': bot_reply})
    
    return jsonify({'reply': bot_reply, 'conversation': session['conversation']})    

@app.route('/clear', methods=['POST'])
def clear():
    session.pop('conversation', None)
    return jsonify({'status': 'success'})

@app.route('/get-conversation', methods=['GET'])
def get_conversation():
    # Return existing conversation without modifying it
    return jsonify({'conversation': session.get('conversation', [])})

if __name__ == '__main__':
    app.run(debug=True)