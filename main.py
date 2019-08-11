import QuizGenerator, json, yaml, db_handler, db_cacher
from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/game', methods=['POST'])
def game():
    category_selection_raw = request.form
    category_selections = []
    for selection in category_selection_raw:
        category_selections.append(selection)
    quiz = QuizGenerator.QuizGenerator(category_selections, config_obj, dbhandler)
    questions_list = quiz.get_questions()
    jsoned_data = json.dumps([q.serialize() for q in questions_list])
    session['questions'] = jsoned_data
    return render_template('game.html', data=jsoned_data)


@app.route('/result', methods=['POST', 'GET'])
def result():
    answers_dict_raw = request.form
    answers_dict = {}
    questions_list = session.get('questions')
    questions_list_ds = json.loads(questions_list)   # ds = DeSerialized

    for answer in answers_dict_raw.keys():
        answers_dict[answer.split('_')[1]] = answers_dict_raw[answer].split('_')[1].strip('"')

    response_json = {}
    for answer in answers_dict:
        question = questions_list_ds[int(answer)-1]
        single_result = {'answered': answers_dict[answer], 'correct': question['name'],
                         'category': config_obj['Categories'][question['category']]['display_name']}
        if answers_dict[answer] == question['name']:
            single_result['result'] = 'true'
        else:
            single_result['result'] = 'false'

        response_json[answer] = single_result

    return render_template('results.html', data=json.dumps(response_json))


@app.route('/perform_cache', methods=['GET'])
def perform_cache():
    db_cacher.start_caching()
    return ('DB is now syncing...')

@app.route('/')
def home():
    return render_template('home.html', data=json.dumps(config_obj['Categories']))


if __name__ == '__main__':
    run_flask = True
    config_obj = None
    dbhandler = None

    dbhandler = db_handler.DBHandler('postgres', 'P@ssw0rd', '127.0.0.1', 'whoinpic_db')
    if not dbhandler.connected:
        print(f"An error occurred while trying to connect to database: {dbhandler.error_msg}")
        exit(1)
    dbhandler.create_tables()
    with open("configuration.yaml", 'r', encoding='utf8') as stream:
        try:
            config_obj = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            print(f'An error occurred reading the configuration file "configuration.yaml": {ex}')

    # dbhandler.clear_table('Persons')
    db_cacher = db_cacher.DB_Cacher(config_obj, dbhandler)
    # db_cacher.start_caching()

    if config_obj and run_flask:
        app.config['config'] = config_obj
        app.config['dbhandler'] = dbhandler
        app.secret_key = 'super secret key'
        app.run(debug=True, host='0.0.0.0', port=8090)

