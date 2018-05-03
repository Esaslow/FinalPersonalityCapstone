import sys
import pickle
from flask import Flask,render_template, request,jsonify,Response
import pandas as pd
import numpy as np

from Friday_MVP_2.src import game
from Friday_MVP_2.src import unpickle

def load_model():
    print('Loading data...')
    file_path = 'Friday_MVP_2/data/2QUestionModel'


    with open(file_path, 'rb') as handle:
        models = pickle.load(handle)
        Traits = pickle.load(handle)
    long_key, questions, grading_Key,\
    keys2trait, Trait_dict_keys, Trait_dict_questions,\
    graded_df, percentile_df, traits_df= unpickle.Load_pickled_files()

    quiz = game.Quiz(questions)
    return long_key, questions, grading_Key,\
    keys2trait, Trait_dict_keys, Trait_dict_questions,\
    graded_df, percentile_df, traits_df, models, Traits, quiz
app = Flask(__name__)


# Endpoints
@app.route('/', methods = ['GET'])
def home():
    return '<h1> Hello WORLDDDD </h1>'

@app.route('/version', methods = ['GET'])
def version():
    return sys.version

# Square a number

quiz = None
@app.route('/Startquiz', methods = ['GET'])
def load():
    print('request recieved')
    global quiz
    quiz = game.Quiz(questions)
    quiz.play_game(models[0],long_key,questions,Traits[0])
    question, flag = quiz.get_question()


    return jsonify({'question':question,'model_number':'0'})

@app.route('/nextQuiz', methods = ['POST'])
def next_quiz():
    global quiz
    req = request.get_json()
    val = req['model_number']
    print(req['model_number'])
    quiz.play_game(models[val],long_key,questions,Traits[val])
    question, flag = quiz.get_question()


    return jsonify({'question':question,'model_number':'0'})

#make a prediction
@app.route('/GetNextQuestion', methods = ['POST'])
def inference():

    req = request.get_json()
    user_value = float(req['user_resp'])/10
    model_val =  int(req['model_number'])

    quiz.change_node(user_value)
    question, flag = quiz.get_question()
    if flag == 0:
        return jsonify({'question':question,'flag':0})
    elif flag == 1:
        string = 'In Trait: '+Traits[model_val] + ', you score in the '+question+'% percentile! '

        print(string)
        return jsonify({'question':string,'flag':0})


#go to about page
@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')

@app.route('/quiz', methods = ['GET'])
def faq():
    return render_template('quiz.html')

@app.route('/mpg', methods = ['GET'])
def mpg():
    return render_template('mpg.html')


#Building the plotting page
@app.route('/plot',methods = ['GET'])
def plot():
    size = list(np.array(quiz.Trait_score)*2)
    text = text = [str(np.round(val,0)) + '% '+Trait for val,Trait in zip(np.array(quiz.Trait_score),quiz.Traits)]
    return jsonify({'size':size,'text':text})

@app.route('/reload',methods = ['GET'])
def reload():
    global model
    model = pickle.load(open('linreg.p','rb'))
    return 'Ok'

if __name__ == '__main__':
    long_key, questions, grading_Key,\
    keys2trait, Trait_dict_keys, Trait_dict_questions,\
    graded_df, percentile_df, traits_df,\
    models, Traits,quiz = load_model()
    print(Traits)
    app.run(host ='0.0.0.0', port = 3333, debug = True)
