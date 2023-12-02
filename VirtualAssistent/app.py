import pyaudio
from flask import Flask, render_template, request
import pandas as pd
import json
import urllib.request
import BusinessLayer.manageTicketBL as CBL
import speech_recognition as sr
import pyttsx3


app = Flask(__name__)
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

'''Chat Bot '''
_chat = dict()


@app.route('/')
def index():
    return render_template('VirtualAgent.html', title="Chat-Bot ")

@app.route('/chat')
def chat():
    return render_template('index.html', title="Chat-Bot ")

@app.route('/whatsapp')
def whatsapp():
    return render_template('whatsappIntegration.html', title="Chat-Bot ")




def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()

def PNRProcess(_outPut, userText):
    if _outPut == "PNR":
        _str = CBL.ticketStatus(_outPut.upper())
        speak("Please provide registered PNR number")
        _chat["PNR"] = ""
    elif _chat["PNR"] == "":
        if CBL.Validate("PNR",userText) == "OK":
            _chat["PNR"] = userText
            speak("Please provide registered your name")
            _str = CBL.ticketStatus("NAME")
            _chat["NAME"] = ""
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This PNR Number does not exist in our system.</div>'

    elif _chat["NAME"] == "":
        if CBL.Validate("NAME", userText) == "OK":
            _chat["NAME"] = userText
            speak("Please provide your date of birth date")
            _str = CBL.ticketStatus("DOB")
            _chat["DOB"] = ""
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This user is not exist in our system.</div>'

    elif _chat["DOB"] == "":
        if CBL.Validate("DOB", userText) == "OK":
            _chat["DOB"] = userText
            speak("Please check your PNR Details")
            _str = CBL.ticketStatus("INFO")
            _chat.clear()
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This user is not exist in our system.</div>'
    return _str

def OrderIdProcess(_outPut, userText):
    if _outPut == "ORDERID":
        _str = CBL.ticketStatus(_outPut.upper())
        speak("Please provide registered Order number")
        _chat["ORDERID"] = ""
    elif _chat["ORDERID"] == "":
        if CBL.Validate("ORDERID", userText) == "OK":
            _chat["ORDERID"] = userText
            speak("Please provide registered your name")
            _str = CBL.ticketStatus("NAME")
            _chat["NAME"] = ""
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This ORDERID Number does not exist in our system.</div>'

    elif _chat["NAME"] == "":
        if CBL.Validate("NAME", userText) == "OK":
            _chat["NAME"] = userText
            speak("Please provide your date of birth date")
            _str = CBL.ticketStatus("DOB")
            _chat["DOB"] = ""
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This user is not exist in our system.</div>'

    elif _chat["DOB"] == "":
        if CBL.Validate("DOB", userText) == "OK":
            _chat["DOB"] = userText
            speak("Please check your Order Number Details")
            _str = CBL.ticketStatus("INFO")
            _chat.clear()
        else:
            _str = '<div class="alert alert-info"><strong>Info!</strong> This user is not exist in our system.</div>'
    return _str

def TNProcess(_outPut, userText):
    if _outPut == "TN":
        speak("Please provide registered Ticket number")
        _str = CBL.ticketStatus(_outPut.upper())
        _chat["TN"] = ""
    elif _chat["TN"] == "":
        if CBL.Validate("TN", userText) == "OK":
            _chat["TN"] = userText
            speak("Please provide registered your name")
            _str = CBL.ticketStatus("NAME")
            _chat["NAME"] = ""
        else:
            _str = "This Ticket Number does not exist in our system."

    elif _chat["NAME"] == "":
        if CBL.Validate("NAME", userText) == "OK":
            _chat["NAME"] = userText
            speak("Please provide your date of birth date")
            _str = CBL.ticketStatus("DOB")
            _chat["DOB"] = ""
        else:
            _str = "This user is not exist in our system."

    elif _chat["DOB"] == "":
        if CBL.Validate("DOB", userText) == "OK":
            _chat["DOB"] = userText
            speak("Please check your Ticket Number Details")
            _str = CBL.ticketStatus("INFO")
            _chat.clear()
        else:
            _str = "This user is not exist in our system."

    return _str

def getDevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))
    p.terminate();


def takeCommand():
    _youSaid=""
    try:
        # Initialize recognizer class (for recognizing the speech)
        recognizer = sr.Recognizer()
        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        with sr.Microphone() as source:
            #print("Listening...")
            recognizer.pause_threshold = 1
            audio_text = recognizer.listen(source,10,4)
            try:
                # using google speech recognition
                _youSaid = recognizer.recognize_google(audio_text,language='en-in')
                print("You Said: " + _youSaid)
            except Exception as e:
                print(e)
                print("Unable to Recognize your voice.")
                return "None"
    except Exception as e:
        print(e)
        _youSaid = "<span style='color:red;'>To get started, connect a microphone</span>";
    return _youSaid

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if userText!="":
        _outPut = CBL.Approve_process(userText.upper())
        #print("Out Put: " + _outPut)
        if ("BYE" in userText.upper()):
            _chat.clear()
            _str = CBL.chat_bow(userText)
        elif _outPut == "TS":
            _chat.clear()
            _chat["TS"] = userText
            _str = CBL.ticketStatus(_outPut.upper())
        elif _outPut == "AT":
            _chat.clear()
            _str = CBL.getTicketsDetails()

        elif (_outPut == "PNR") or ("PNR" in _chat):
            _str = PNRProcess(_outPut, userText)


        elif _outPut == "ORDERID" or ("ORDERID" in _chat):
            _str = OrderIdProcess(_outPut, userText)

        elif _outPut == "TN" or ("TN" in _chat):
            _str = TNProcess(_outPut, userText)

        elif "Approve" in userText.split("_"):
            _str = CBL.getuserdetails(userText.split("_")[1])
        else:
            _str = CBL.chat_bow(userText)

        print(_chat)
    return _str.strip()
    'return str(CBL.Approve_process(userText.lower()))'

@app.route("/speech")
def Sppech():
    return takeCommand().lower()


'''End'''

if __name__ == '__main__':
    getDevices();
    app.run(host='0.0.0.0', port=8082)

