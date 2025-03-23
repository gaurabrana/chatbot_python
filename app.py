from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_session import Session  # Import Flask-Session

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = "d8c3b880ca6b8a49566a821708c024eb"  # Necessary for using session
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'  # Use the file system to store sessions
app.config['SESSION_PERMANENT'] = False    # Sessions will not persist across restarts
Session(app)  # Initialize server-side session

# Basic HTML rendering
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Basic route for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()  # Convert to lowercase for easier matching

    # Initialize session memory if not present
    if 'conversation' not in session:
        session['conversation'] = []

    # Append the user's message to the conversation
    session['conversation'].append({'sender': 'user', 'message': user_message})

    responses = {
        "hello": "Hi there! How can I assist you?",
        "how are you": "I'm just a bot, but I'm functioning perfectly!",
        "bye": "Goodbye! Have a great day!"
    }

    # Find a matching response or return a default
    bot_reply = responses.get(user_message, "I didn't quite understand that. Can you try again?")
    
    # Append the bot's response to the conversation
    session['conversation'].append({'sender': 'bot', 'message': bot_reply})

    return jsonify({
        'reply': bot_reply,
        'conversation': session['conversation']  # Return the full conversation history
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)