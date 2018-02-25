from flask import Flask,jsonify, flash, redirect,url_for
from flask import request
from flask import render_template
from sklearn.externals import joblib
import string


app = Flask(__name__)

model_load = joblib.load('sentiment_model.pkl')

label_dict = {"0":"Negative",
              "1":"Somewhat Negative",
              "2":"Neutral",
              "3":"Somewhat Positive",
              "4":"Positive"
             }

def preprocess_string(x):
    punctuations = '''!()-[]{};:\n'\t"\,<>./?@#+$%^&*_~'''
    no_punct = ""
    for char in x:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct.lower()

def prediction(s):
    label = model_load.predict([s])
    return str(label)


@app.route('/')
def my_form():
    return render_template("index.html")


@app.route('/', methods=['GET','POST'])
def my_form_post(): 
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        processed_text =  preprocess_string(text)
        print(processed_text)
        prediction_text = prediction(processed_text)
        print(prediction_text[1])
        sentiment = label_dict.get(prediction_text[1])
        print(sentiment)
        return render_template('index.html', review=text, output=sentiment)
    else:
        return render_template('index.html', review=text, output=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)