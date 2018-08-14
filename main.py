# [START app]
import base64
import json
import logging
import os

from flask import current_app, Flask, render_template, request
from google.cloud import pubsub


import requests

from zaifapi import *
import datetime

app = Flask(__name__)

# Configure the following environment variables via app.yaml
# This is used in the push request handler to veirfy that the request came from
# pubsub and originated from a trusted source.

app.config['PUBSUB_TOPIC'] = os.environ['PUBSUB_TOPIC']
app.config['PROJECT'] = os.environ['GOOGLE_CLOUD_PROJECT']


data = ""

# [START index]
@app.route('/', methods=['GET'])
def index():

    global data

    btcjpy = 0
    ethjpy = 0
    zaif = ZaifPublicApi()
    btcjpy = zaif.last_price('btc_jpy')
    btcjpy_i = btcjpy['last_price']
    ethjpy = zaif.last_price('eth_jpy')
    ethjpy_i = ethjpy['last_price']
    now = datetime.datetime.now()
    created = now.strftime("%Y-%m-%d %H:%M:%S")

    json_str = ""

    json_dict = dict(timestamp=created,btc_jpy=btcjpy_i,eth_jpy=ethjpy_i)
    json_str = str(json_dict).replace("\'","\"")

    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(
        current_app.config['PROJECT'],
        current_app.config['PUBSUB_TOPIC'])

    data = json_str.encode('utf-8')
    publisher.publish(topic_path, data=data)
    print("instance process finish")

    return 'OK', 200
# [END index]


@app.errorhandler(500)
def server_error(e):
    print('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
