# Updated Flask app
from flask import Flask, request, jsonify, send_from_directory, session
from flask_session import Session
from datetime import timedelta
from utils.ai_model import HybridAssistant
from utils.flask_secret_key import ensure_secret_key, load_secret_key

ensure_secret_key()

app = Flask(__name__, static_folder='static')
app.secret_key = load_secret_key()

# Session Config (still needed for multi-user support)
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
    user_message = request.json.get('message', '').strip()
    
    # Initialize conversation history if not exists
    if 'conversation' not in session:
        session['conversation'] = []
    
    # Add user message to history
    if user_message:
        session['conversation'].append({'sender': 'user', 'message': user_message})
    
    # Generate response with full context
    bot_reply = assistant.generate_response(
        user_message,
        session['conversation']
    )
    
    # Add bot response to history
    session['conversation'].append({'sender': 'bot', 'message': bot_reply})
    
    # Trim history if too long (last 6 exchanges)
    if len(session['conversation']) > 12:
        session['conversation'] = session['conversation'][-12:]
    
    session.modified = True
    return jsonify({
        'reply': bot_reply,
        'conversation': session['conversation']
    })

@app.route('/clear', methods=['POST'])
def clear():
    session.pop('conversation', None)
    return jsonify({'status': 'success'})

@app.route('/get-conversation', methods=['GET'])
def get_conversation():
    return jsonify({'conversation': session.get('conversation', [])})

if __name__ == '__main__':
    app.run(debug=True)