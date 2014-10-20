from flask import Flask, render_template, Response, request
from werkzeug.serving import BaseHTTPRequestHandler
from twitter import Twitter, OAuth
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

oauth_conf = dict(config['oauth'])
server_conf = dict(config['server'])
config.pop('oauth')
config.pop('server')

consumer_key = oauth_conf['consumer_key']
consumer_secret = oauth_conf['consumer_secret']

clients = {}
for section in config.sections():
    atoken = config[section]['access_token']
    asecret = config[section]['access_token_secret']
    clients[section.lower()] = \
        Twitter(auth=(OAuth(atoken, asecret, consumer_key, consumer_secret)))

app = Flask(__name__)


def update_with_media(client, status, media):
    twitter = clients[client.lower()]
    return twitter.statuses.update_with_media(**{'status': status,
                                                 'media[]': media})


@app.route('/', methods=['POST'])
def upload():
    msg = request.form['message']
    user = request.form['username']
    img = request.files['media'].stream.read()
    api_response = update_with_media(user, msg, img)
    if 'media' in api_response['entities']:
        image_url = api_response['entities']['media'][0]['display_url']
    else:
        image_url = api_response['entities']['urls'][-1]['display_url']
    xml = render_template('result.xml', image_url=image_url)
    response = Response(xml, mimetype='application/xml')
    return response

if __name__ == '__main__':
    server_conf['port'] = int(server_conf.get('port', '5000'))
    app.run(**server_conf)
