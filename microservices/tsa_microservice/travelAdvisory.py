import os

import pika
import requests
from bs4 import BeautifulSoup

#This CLOUDAMQP_URL is my personal server, you may change the URL if you wish to host it on your own server
#-----------------------------------------------
url = os.environ.get('CLOUDAMQP_URL', 'amqps://cgbguoip:VoHZcopUZ_IiWlb1CmcQ1Ip4JBbD830F@beaver.rmq.cloudamqp.com/cgbguoip')
params = pika.URLParameters(url)
params.socket_timeout = 5
connection = pika.BlockingConnection(params)
#-----------------------------------------------

channel = connection.channel()

channel.queue_declare(queue='advisory')


def tsa_precaution(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        headline = soup.find_all(class_="tsg-rwd-emergency-alertheader-title")
        headline= str(headline[0])
        advisory = headline[48:-5]
        color = level_color(advisory)

        date = soup.find_all(class_="tsg-rwd-emergency-alertheader-type-frame-typebox alerttype")
        date = (str(date[0]))[92:-6]
        #date = date[92:-6]
        #print(date[92:-6])
        response_dict = {
            'advisory': advisory,
            'color': color,
            'date': date,
            'url': url,
        }
        return str(response_dict)

    except:
        return('fail')


def level_color(headline):
    if '1' in headline:
        return("blue")
    elif '2' in headline:
        return("yellow")
    elif '3' in headline:
        return("orange")
    else:
        return("red")

def on_request(ch, method, props, body):
    country = str(body.decode())   #body.decode() gets rid of binary encoding
    print("Received request for %s" % country)

    url = ("https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/%s-travel-advisory.html" %country)
    try:
        response = tsa_precaution(url)
    except:
        response = "This TSA travel advisory not found"
        print(response)
        return response
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='advisory', on_message_callback=on_request)

try:
    print("Travel Advisory Mircorservice is currently listening for requests... \nTo terminate, press Ctrl C")
    channel.start_consuming()

except KeyboardInterrupt:
    print("CTRL C caught, Travel Advisory Microservice is now terminating")
