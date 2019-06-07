from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/sms",methods = ['POST'])
def sms_reply():
        #fetch message from post request
    #print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    # Create reply
    resp = MessagingResponse()
    resp.message(fetch_reply(msg, sender))
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True,use_reloader = True)
