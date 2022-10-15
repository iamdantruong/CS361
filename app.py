from flask import Flask, render_template, redirect, request
import requests
import json

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
        #country_json = {'country': country}
        #url = 'http://localhost:5001'
        #request = requests.post(url, json= country_json)
        #response= request.json()
        #response_summary = response['summary'] #(str)
        #response_cities = response['cities'] #(list)
        
        return redirect ('/country/'+countryName, )#summary= response_summary, cities = response_cities)
    return render_template("index.html")

# def wikiService(requestString):
#     #####
#     #My Microservice, Functional
#     ##### 
#     url = "http://localhost:1400"
#     itemDict = {"item": str(requestString)}
#     postItem = requests.post(url,data=itemDict)
#     postRes = postItem.json()
#     resStr = str(postRes["item"])
#     return(resStr)

@app.route('/country/<countryName>')
def country(countryName):
    countryName= countryName.replace('_',' ')
    #country_json = json.dumps( {'country': countryName})
    url = 'http://localhost:5001'
    country_dict = {'country': str(countryName)}
    request = requests.post(url, data= country_dict)
    print("Sending request to wiki microservice on port 5001:",request)
    response= request.json()
    print("Received response from port port 5001: ", response)
    response_summary = response['summary'] #(str)
    response_cities = response['cities'] #(list)
    return render_template("countries.html", countryName= countryName, summary= response_summary, cities = response_cities)

@app.route('/planner')
def planner():
    return render_template("planner.html")

if __name__ == '__main__':
   app.run()