import flask
from flask import request, session
import requests as req
import json
import random
import secrets
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
#set stats field
session = { 'requests': 0, 'distributions': []}

#return a random chuck norris joke.
def chuck_api():
    try:
        res = req.get('https://api.chucknorris.io/jokes/random')
        res.raise_for_status()
    except:
        return 404
    return res.text

#return a random kanye west quote.
def kanye_api():
    try:
        res = req.get('https://api.kanye.rest')
        res.raise_for_status()
    except:
        return 404
    return res.text

#return the sum of letters converted to a number (‘A’='a'=1, ‘B’='b'= 2, 'C'='c'=3)
def name_sum_api(name):
    name = name.replace(" ","")
    name_by_num = [ord(c)%32 for c in name]
    return sum(name_by_num)

#update session for stats by location of surprising type
def update_sess(surprise_loc):
    #if first successful call to surprise
    if session['requests'] == 0:
        session['distributions'] = [{'type':'chuck-norris-joke', 'count': 0},{'type':'kanye-quote', 'count': 0},{'type':'name-sum', 'count': 0}]
    session['requests'] += 1
    session['distributions'][surprise_loc]['count'] += 1

    
@app.route('/api/surprise', methods=['GET'])
def api_surpise():
    status_code = 200
    err = 'Error: '
    #check valid name
    if 'name' in request.args:
        name = request.args['name']
        if not name.replace(" ","").isalpha():
            status_code = 400
            err += ' name must contain only alphabets '   
    else:
        status_code = 400
        err += ' no name field provided '

    #check valid birth_year
    if 'birth_year' in request.args:
        birth_year = request.args['birth_year']
        try:
            birth_year = int(request.args['birth_year'])
            if birth_year < 1900 or birth_year > 2020:
                status_code = 400
                err += ' birth year must be in range 1900-2020'
        except:
            status_code = 400
            err += ' birth_year must contain only digits '
    else:
        status_code = 400
        err += ' no birth_year field provided '

    #if the input is not valid - return error 400 informative message
    if status_code == 400:
        return err, status_code

    #options contain all the avaliable surprsing options for the user
    options = []
    first_char = name[0]
    if ((first_char != 'A') and (first_char != 'Z') and (birth_year > 2000)):
        options.append('kanye')
    if (first_char != 'Q'):
        options.append('name_sum')
    if (birth_year <= 2000):
        options.append('chuck')

    #choose a random option, if error - try another option if exists
    while options:
        chosen_surprise = random.choice(options)
        
        #in case that name sum chosen
        if chosen_surprise == 'name_sum':
            update_sess(2)
            dict_name_sum = {'type': 'name-sum' , 'result': name_sum_api(name)}
            return json.dumps(dict_name_sum)

        #in case that kanye west chosen
        if chosen_surprise == 'kanye':
            kanye = kanye_api()
            if kanye is not 404:
                k_json = json.loads(kanye)
                update_sess(1)
                dict_kanye = {'type': 'kanye-quote' , 'result': k_json['quote']}
                return json.dumps(dict_kanye)
            options.remove('kanye')
                
        #in case that chuck norris chosen
        if chosen_surprise == 'chuck':
            chuck = chuck_api()
            if chuck is not 404:
                c_json = json.loads(chuck)
                update_sess(0)
                dict_chuck = {'type': 'chuck-norris-joke' , 'result': c_json['value']}
                return json.dumps(dict_chuck)
            options.remove('chuck')

    #if no surprise returned - return error 404 informative message
    status_code = 404
    return 'No surprise for you! ' , status_code
        
@app.route('/api/stats', methods=['GET'])
def api_stats():
    status_code = 200
    return json.dumps(session)

    
app.run(host="localhost", port=3000, debug=True)
