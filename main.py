import QuizGenerator, json
from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/game', methods=['POST'])
def game():
    quiz = QuizGenerator.QuizGenerator('Israeli_Actresses')
    questions_list = quiz.get_questions()
    jsoned_data = json.dumps([q.serialize() for q in questions_list])
    session['questions'] = jsoned_data
    return render_template('game.html', data=jsoned_data)


@app.route('/result', methods=['POST'])
def result():
    answers_dict = request.form
    questions_list = session.get('questions')
    response = ''

    for answer in answers_dict.keys():
        response += answer + '\n'


    return 'submitted answeres: {}\nQuestions were: {}.'.format(response,questions_list)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, host='0.0.0.0', port=8090)
