import QuizGenerator, json
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/game', methods=['POST'])
def game():
    quiz = QuizGenerator.QuizGenerator('Israeli_Actresses')
    questions_list = quiz.get_questions()
    return render_template('game.html', data=json.dumps([q.serialize() for q in questions_list]))

# for person in questions_list:
#     print(f'{person.name}, {person.image_url}, {person.options}')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090)
