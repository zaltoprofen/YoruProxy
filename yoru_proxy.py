from flask import Flask, render_template, Response, request
from werkzeug.serving import BaseHTTPRequestHandler
from twitter import Twitter, OAuth
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

oauth_conf = config['oauth']
server_conf = config['server']

access_token = oauth_conf['access_token']
access_token_secret = oauth_conf['access_token_secret']
consumer_key = oauth_conf['consumer_key']
consumer_secret = oauth_conf['consumer_secret']

app = Flask(__name__)
twitter = Twitter(auth=OAuth(access_token, access_token_secret,
                             consumer_key, consumer_secret))


def update_with_media(status, media):
    return twitter.statuses.update_with_media(**{'status': status,
                                                 'media[]': media})


@app.route('/', methods=['POST'])
def upload():
    msg = request.form['message']
    img = request.files['media'].stream.read()
    api_response = update_with_media(msg, img)
    image_url = api_response['extended_entities']['media'][0]['display_url']
    xml = render_template('result.xml', image_url=image_url)
    response = Response(xml, mimetype='application/xml')
    return response

if __name__ == '__main__':
    server_conf = dict(server_conf)
    server_conf['port'] = int(server_conf.get('port', '5000'))
    app.run(**server_conf)
