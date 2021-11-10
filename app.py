import boto3
import json
#crop recommendation app
#app.py page
from flask import Flask,render_template,request
#for api
import requests
import config

import numpy as np

app=Flask(__name__)

@app.route('/')#main web page
def home():
    return render_template('input.html')


@app.route('/translate',methods=['GET','POST']) #rendering prediction page
def translate():
    if request.method=='POST':
        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
        text=str(request.form['Text'])
        source=str(request.form['Source'])
        target=str(request.form['Target'])
        result = translate.translate_text(Text=text, 
            SourceLanguageCode=source, TargetLanguageCode=target)
        final_prediction=result.get('TranslatedText')
        return render_template('translate.html', prediction=final_prediction)


@app.route('/sentiment',methods=['GET','POST'])
def sentiment():
    if request.method=='POST':
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        txt=str(request.form['Text'])
        result=json.dumps(comprehend.detect_sentiment(Text=txt, LanguageCode='en'), sort_keys=True, indent=4)
        return render_template('translate.html', prediction=result)



#running the app
if __name__ == '__main__':
    app.run(debug=True,port=5500)
