from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import requests
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # secret key config
app.config['SESSION_TYPE'] = 'filesystem' # stockage de la session
Session(app)

# Initialize the limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address
)

metrics = PrometheusMetrics(app)

def encode_credentials(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def main_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        encoded_credentials = encode_credentials(username, password)

        # Store the encoded credentials in the session
        session['encoded_credentials'] = encoded_credentials

        return redirect('/microc/list_medias')
    
    return render_template('media.html')

@app.route('/list_medias', methods=['GET'])
@limiter.limit("20 per minute")
def list_medias():
    # Get the encoded credentials from the session
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect('/microc')

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = 'http://wordpress:80/wp-json/wp/v2/media'
    response = requests.get(url, auth=(username, password))
    medias = response.json()
    return render_template('list_medias.html', medias=medias, encoded_credentials=encoded_credentials)

@app.route('/update_media/<int:media_id>', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def update_media(media_id):
    # Get the encoded credentials from the session
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect('/microc')

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    if request.method == 'POST':
        title = request.form.get('title')
        alt_text = request.form.get('alt_text')
        url = f'http://wordpress:80/wp-json/wp/v2/media/{media_id}'
        data = {
            'title': {'raw': title},
            'alt_text': alt_text
        }
        response = requests.put(url, json=data, auth=(username, password))
        if response.status_code == 200:
            return redirect('/microc/list_medias')
    
    url = f'http://wordpress:80/wp-json/wp/v2/media/{media_id}'
    response = requests.get(url, auth=(username, password))
    media = response.json()
    return render_template('update_media.html', media=media, media_id=media_id, encoded_credentials=encoded_credentials)

@app.route('/delete_media/<int:media_id>', methods=['GET'])
@limiter.limit("20 per minute")
def delete_media(media_id):
    # Get the encoded credentials from the session
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect('/microc')

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = f'http://wordpress:80/wp-json/wp/v2/media/{media_id}'
    response = requests.delete(url, auth=(username, password))
    return redirect('/microc/list_medias')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)
