from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def read_keywords(file_path):
    keywords = {}
    with open(file_path, encoding='utf-8') as f:
        lines = f.read().splitlines()
    for line in lines:
        keyword, *answers = line.split(';')
        keywords[keyword.lower()] = answers
    print("Keywords:", keywords)
    return keywords

def get_response(user_input, keywords):
    user_input = user_input.lower().rstrip('?')
    user_input = user_input.lower().rstrip('!')
    user_input = user_input.lower().rstrip('.')
    user_input = user_input.lower().rstrip(',')
    user_input = user_input.lower().rstrip('?!')
    response = "Извините, я не знаю, что ответить."
    if user_input in keywords:
        response = random.choice(keywords[user_input])
    return response


file_path = 'dialogues.txt'
keywords = read_keywords(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_input = request.json.get('user_input')
    print("User input:", user_input)
    response = get_response(user_input, keywords)
    print("Bot response:", response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)