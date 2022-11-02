import datetime

import requests
from flask import Flask, render_template, redirect, request

import microservices.tsa_microservice.send_country as send_country
from microservices.currency_microservice.currency_exchange_client import *
from sandbox import *
from validation import *

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/home')

@app.route('/home')
def home2():
    return render_template("home.html")

@app.route('/country', methods= ['GET','POST'])
def index():
    if request.method=='POST': #and validate form for country
        countryName = request.form.get('country')

        if validate_country(countryName):
            countryName = countryName.capitalize()
            return redirect ('/country/'+countryName)
        else:
            return redirect ('/error')
    return render_template("index.html")

@app.route('/error', methods= ['GET', 'POST'])
def error():
    return render_template('error.html')

@app.route('/country/<countryName>', methods=['GET', 'POST'])
def country(countryName):
    temp_dict = {}
    curr_dict = {}

    #---------------------------------------------------
    if request.method=='POST' and 'weather' in request.form:
        date= request.form.get('date')
        location = request.form.get('location').split(",")
        location_city= location[0]
        location_country= location[1]
        
        temp_data = get_weather(date, location_city, location_country)
        temp_dict = {
            'country': location_country,
            'city': location_city,
            'date': temp_data[3],
            'tavg': temp_data[0],
            'tmin': temp_data[1],
            'tmax': temp_data[2],
        }
    #-------------------------------------------------------------

    if request.method=='POST' and 'currency' in request.form:
        amount = float(request.form.get('quantity'))
        from_curr= request.form.get('from_curr')
        to_curr= request.form.get('to_curr')
        today = f"{datetime.now():%Y-%m-%d %H:%M}"
        try:
            curr = CurrConverter(from_curr, to_curr, amount)
            curr_response = json.loads(curr.exchange())
        #{'total': 1338.1077264474484, 'rate': 148.6786362719387}
            curr_dict= {
                'exchange_rate': "%.2f" %curr_response['rate'],
                'amount': amount,
                'from_curr': from_curr,
                'exchange_value': "%.2f" %curr_response['total'],
                'to_curr': to_curr,
                'date': today
            }
        except:
            curr_dict= {
                'exchange_rate': "Error, currency is not available",
                'amount': amount,
                'from_curr': from_curr,
                'exchange_value': "Error!",
                'to_curr': to_curr,
                'date': today
            }
    countryName= countryName.replace('_',' ')

    if not validate_country(countryName):
        return redirect ('/error')
    
    tsa_country = countryName.replace(' ','-')
    tsa_country = tsa_country.lower()

    #--------------------------------#
    #passing in currency
    currency = [curr_name[country_curr[countryName]], country_curr[countryName]]
    all_currencies = curr_name
    #currency is a list like [US Dollar, USD] 
    #all_currencies is a dictionary like {'USD' : 'US Dollar', }

    #--------------------------------#
    #microservice request to wikiServer.py
    url = 'http://localhost:5001'
    country_dict = {'country': str(countryName)}
    req = requests.post(url, data= country_dict)
    response= req.json()
    response_summary = response['summary'] #(str)
    response_cities = response['cities'] #(list)

    #--------------------------------#
    #microservice request to travelAdvisory.py
    rpc = send_country.SendCountryClient(tsa_country)
    response_t = rpc.call()
    
    return render_template("countries.html", countryName= countryName, summary= response_summary, cities = response_cities, advisory= response_t, currency = currency, all_currencies = all_currencies, temperature= temp_dict, curr_dict = curr_dict)

@app.route('/planner')
def planner():
    return render_template("planner.html")

if __name__ == '__main__':

    app.run()