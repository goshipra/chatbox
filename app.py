from flask import Flask, render_template,request,jsonify
import json
from flask_cors import CORS
import requests
from pprint import pprint
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from markupsafe import Markup

url = "https://itu.peoplereign.io/message?virtualAgentID=peoplereign&clientType=html"
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBsaWNhdGlvbiI6InZpcnR1YWxfYWdlbnQiLCJjbGllbnQiOiJzZXJ2aWNlbm93IiwiaXNzIjoiUjNOUnhleGFvckJ3NFR6Y2o3YTNTelFVbmNXd0I4WEEifQ.ErjYIbXyrVUbAezPWgXo1f5mmV4vwVJIbnHJLV-jT8g'
POST_HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
SSL_VERIFY = False

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('base.html')

@app.route("/predict", methods=['POST','GET'])
def predict():

    text= request.get_json().get("message")
    print( "user message: ",text)


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
    pprint(AllContent)
    chatbotAnswer = AllContent['snippet']['content']
    predictedAnswer = Markup(chatbotAnswer)
    print(chatbotAnswer)

    LinkedSnippetList = []
    linkedSnippets = AllContent['snippet']['linkedSnippets']
    if not linkedSnippets:
        print("No options")
    else:
        print("Select from below options:")
        for snippet in  linkedSnippets:
            LinkedSnippetList.append(snippet['promptText'])



    response = predictedAnswer
    message = {"answer": response,"options":LinkedSnippetList}
    print(message)
    return jsonify(message)

if __name__ == '__main__':
    app.run()

