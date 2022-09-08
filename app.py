#!/usr/bin/env python3
# app.py
# Author : Shipra Rathore

# importing necessary libraries
from flask import Flask, render_template, request, jsonify  # flask modules
import json
from flask_cors import CORS
import requests
from pprint import pprint
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from markupsafe import Markup

# people reign API url, Token, Post headers
url = "https://itu.peoplereign.io/message?virtualAgentID=peoplereign&clientType=html"
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBsaWNhdGlvbiI6InZpcnR1YWxfYWdlbnQiLCJjbGllbnQiOiJzZXJ2aWNlbm93IiwiaXNzIjoiUjNOUnhleGFvckJ3NFR6Y2o3YTNTelFVbmNXd0I4WEEifQ.ErjYIbXyrVUbAezPWgXo1f5mmV4vwVJIbnHJLV-jT8g'
POST_HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}',
                "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*"}
SSL_VERIFY = False

# flask app
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST', 'GET', 'HEAD'])
def home():
    """
    Main home page
    """
    return render_template('base.html')


@app.route('/greetings', methods=['POST', 'GET', 'HEAD'])
def greetings():
    """
    Prints greetings in chatbot when user presses chat button. details of json_data_greeting
    can be changed or left empty.
    """
    json_data_greeting = json.dumps({"user": {"firstName": "Shipra", "lastName": "Rathore", \
                                              "email": "rathoreshipra7061@students.itu.edu"}, \
                                     "languageCode": "en", "type": "greeting", \
                                     "content": ''})

    results = requests.post(
        url,
        verify=SSL_VERIFY,
        data=json_data_greeting,
        headers=POST_HEADERS
    )

    # pprint(results.json())
    # json data from API
    AllContent = results.json()
    # pprint(AllContent)
    chatbotAnswer = AllContent['greeting']['content']
    predictedAnswer = Markup(chatbotAnswer)
    print(chatbotAnswer)
    response = predictedAnswer
    message = {"answer": response, "options": ' '}
    print(message)
    return jsonify(message)


@app.route("/predict", methods=['POST', 'GET', 'HEAD'])
def predict():
    """
    fetch message from user and calls people reign API to get the answer and
    return the answer to chat bot
    """

    text = request.get_json().get("message")
    print("user message: ", text)

    json_data = json.dumps({"user": {"firstName": "Shipra", "lastName": "Rathore", \
                                     "email": "rathoreshipra7061@students.itu.edu"}, \
                            "languageCode": "en", "type": "message", \
                            "content": text})

    results = requests.post(
        url,
        verify=SSL_VERIFY,
        data=json_data,
        headers=POST_HEADERS
    )

    # pprint(results.json())
    # json data from API
    AllContent = results.json()
    # pprint(AllContent)
    chatbotAnswer = AllContent['snippet']['content']
    print(chatbotAnswer)
    predictedAnswer = Markup(chatbotAnswer)
    print(chatbotAnswer)
    response = predictedAnswer

    LinkedSnippetList = []
    linkedSnippets = AllContent['snippet']['linkedSnippets']
    print(LinkedSnippetList)
    if not linkedSnippets:
        print("No options")
        message = {"answer": response, "options": ' '}
        print(message)
        return jsonify(message)
    else:
        print("Select from below options:")
        for snippet in linkedSnippets:
            LinkedSnippetList.append(snippet['promptText'])
        message = {"answer": response, "options": LinkedSnippetList}
        print(message)
        return jsonify(message)


if __name__ == '__main__':
    """ Driver code"""
    app.run(debug=True)
