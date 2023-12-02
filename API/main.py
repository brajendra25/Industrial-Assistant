# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pandas as pd
import re
import nltk

'''nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')'''
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from datetime import datetime

# creating a Flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

_data = {"TN": "12345", "ORDERID": "12345", "PNR": "12345", "NAME": "Nitin", "DOB": "25/11/1987",
         "TS": "Confirmed", "Departure Time": "8:00 PM"}
_user1 = {"TN": "456789", "ORDERID": "456789", "PNR": "123456789", "NAME": "Ram", "DOB": "25/11/1986",
          "TS": "Confirmed", "Departure Time": "8:00 PM"}
_tickets = [_data, _user1]

_clientName = ''


@app.route('/Validate/', methods=['GET'])
def Validate():
    try:
        _value = None
        _parameters = request.args.to_dict()
        for x, y in _parameters.items():
            print(x)
            print(y)
            if x.upper() == "NAME":
                _value = getNameFromSen(y)
                _clientName = _value
            elif x.upper() == "DOB":
                _value = getDateFromSentance(y)
            print(_value)
            if _value is None:
                _value = y
            if _data[x.upper()].upper() == _value.upper().strip():
                return "OK"
            else:
                return "NOT OK"
    except Exception as e:
        print(e)
        return str(e)


@app.route('/getresponse/', methods=['GET'])
def getresponse():
    try:
        userInput = request.args.get("userinput")
        if userInput == "TS":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box " \
                   "message-partner'>Please provide us any one of these : " \
                   + "<p id='dvOrderId' class='message-options-button' onclick=action(this)><span>Order Id</span></p>" \
                   + "<p id='dvPNR' class='message-options-button' onclick=action(this)><span>PNR</span></p> " \
                   + "<p id='dvTN'  class='message-options-button' onclick=action(this)><span>Ticket Number</span></p> " \
                     "</div></div> "
        elif userInput == "PNR":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box " \
                   "message-partner'>Please provide PNR Number only : </div></div> "
        elif userInput == "ORDERID":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box " \
                   "message-partner'>Please provide Order Id only : </div></div> "

        elif userInput == "TN":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box " \
                   "message-partner'>Please provide your Ticket Number only : </div></div> "

        elif userInput == "NAME":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box message-partner'>Please provide your " \
                   "Full Name (As Record) : </div></div> "
        elif userInput == "DOB":
            _str = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box message-partner'>Hi " + _clientName + " Please provide your " \
                                                                                                                                                         "DOB only (MM/dd/yyyy)(As Record) : </div> </div>"
        elif userInput == "INFO":
            _msg = "<div class='message-sender'>Agent</div><div class='message-box-holder'><div class='message-box message-partner'>Thanks, Please wait " \
                   "we are trying to get your information :</div></div> "
            _str = _msg + pd.DataFrame([_data])
            _str = _msg + getstatus() + "<br /><div class='message-box-holder'><div class='message-box " \
                                        "message-partner'>Thanks.<br /> </div></div>"

        return _str
    except:
        return "500"  # Service Error Code


def getNameFromSen(_sen):
    text = _sen
    nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
            # print('Type: ', nltk_result.label(), 'Name: ',  name.strip())
            return name


def getDateFromSentance(_sen):
    # searching string
    match_str = re.findall(r'\d+\S\d+\S\d+', _sen)
    # computed date
    # feeding format
    print(match_str[0])
    return match_str[0]


@app.route('/getstatus')
def getstatus():
    try:
        _df = pd.DataFrame([_data])
        _html = ""
        _table = '<div class="message-sender">Agent</div><div class="message-box-holder"><div class="message-box ' \
                 'message-partner"><table class="table table-bordered"> '
        _end = '</div></div></table>'
        for key, value in _data.items():
            if key == "TN":
                key = "Ticket Number"
            if key == "ORDERID":
                key = "Order Id"
            if key == "TS":
                key = "Current Status"
            _html = _html + '<tr><td style="font-weight:bold;">' + key + '</td><td>' + value + '</td></tr>'
        _details = _table + _html + _end
        return "<br/><div class=''>" + _details + "</div>"
    except:
        return "500"  # Service Error Code


@app.route('/getTicketsDetails')
def getTicketsDetails():
    df = pd.DataFrame([[_tickets]])
    _html = ""
    _table = '<div class="message-sender">Agent</div><div class="message-box-holder"><div class="message-box ' \
             'message-partner"><table class="table table-bordered"> '
    _end = '</div></div></table>'
    for item in _tickets:
        for key, value in item.items():
            _html = _html + '<tr><td style="font-weight:bold;"><p>Ticket</p></td><td><p class="btn btn-primary" onclick="approveTickets(this);" id="' + value + '"' + ">Approve</p>" + '</td></tr>'
            break;
    _details = _table + _html + _end
    return "<br/><div class=''>" + _details + "</div>"


@app.route('/getuserdetails')
def getuserdetails():
    ticketNo = request.args.get("ticketNo")
    print(ticketNo)
    _html = ""
    _table = '<div class="message-sender">Agent</div><div class="col-lg-10"><div class="message-box-holder"><div class="message-box ' \
             'message-partner">'
    _end = '<div class="btn btn-primary right" onclick="GetApprove();">Approve</div></div></div></div>'
    for item in _tickets:
        for key, value in item.items():
            if value == ticketNo:
                df = pd.DataFrame([item])
                df = df.drop(df.columns[[0, 1]], axis=1)
                return _table + df.to_html(classes='table table-stripped') + _end


# driver function
if __name__ == '__main__':
    app.run(debug=True)
