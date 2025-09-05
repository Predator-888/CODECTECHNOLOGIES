# Add render_template to this import line
from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS
from chatbot import Chatbot
from database import log_interaction

app = Flask(__name__)
CORS(app) 

print("Loading chatbot model...")
bot = Chatbot('intents.json')
print("Chatbot model loaded.")

# ADD THIS NEW ROUTE
@app.route('/')
def home():
    # This will serve the index.html file from the 'templates' folder
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    bot_response = bot.get_response(user_message)
    log_interaction(user_message, bot_response)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)