from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)  
genai.configure(api_key="AIzaSyCn-46zc9Ct3ssoe4y6KGh9zM0wc-7soEc")
model = genai.GenerativeModel("gemini-1.5-flash")

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()  # safer with default empty string

    conversation_history.append(user_input)  # store raw user input

    prompt = "\n".join(conversation_history)

    response = model.generate_content(prompt)

    bot_reply = response.text if hasattr(response, "text") else ""

    # If bot_reply starts with "Bot:", remove it to avoid double prefix
    if bot_reply.startswith("Bot:"):
        bot_reply = bot_reply[len("Bot:"):].strip()

    conversation_history.append(bot_reply)  # store raw bot reply

    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
