#This code has been adapted from RabbitMQ Remote Procedure Calls tutorials https://www.rabbitmq.com/tutorials/tutorial-six-python.html

import json
import os
import uuid

import pika


class SendCountryClient(object):
    #Defines the class and methods for a client that sends a zip code to various openweather API and returns the response in json format.

    def __init__(self, country):
        #(Use this if you would prefer to host microservice on local host)
        #-----------------------------------------------
        #self.connection = pika.BlockingConnection(
        #    pika.ConnectionParameters(host='localhost'))
        #-----------------------------------------------
        

        #This CLOUDAMQP_URL is my personal server, you may change the URL if you wish to host it on your own server
        #-----------------------------------------------
        url = os.environ.get('CLOUDAMQP_URL', 'amqps://cgbguoip:VoHZcopUZ_IiWlb1CmcQ1Ip4JBbD830F@beaver.rmq.cloudamqp.com/cgbguoip')
        params = pika.URLParameters(url)
        params.socket_timeout = 5
        self.connection = pika.BlockingConnection(params)
        #-----------------------------------------------

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
        self.country = str(country)
    
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='advisory',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=self.country)
        self.connection.process_data_events(time_limit=None)
        response= json.loads(self.response.decode().replace("\'", "\""))
        return response


#rpc = SendCountryClient('japan')
#response = rpc.call()
#print(response['advisory'])
#print(response['date'])
#print(response['color'])

