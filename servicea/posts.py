from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import requests
import base64
import os

# Initialisation de la session Flask côté serveur
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # secret key config
app.config['SESSION_TYPE'] = 'filesystem' # stockage de la session
Session(app)

# Initialisation du limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address
)

# Intégration de la route /metrics pour le monitoring Prometheus
metrics = PrometheusMetrics(app)

# Encodage des credentials
def encode_credentials(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials

# Route principale (main page)
@app.route('/', methods=['GET', 'POST'])
@limiter.limit("20 per minute") # Limit rate de requête de l'adresse par IP
def main_page():
    if request.method == 'POST': # Fonction pour se connecter
        username = request.form.get('username')
        password = request.form.get('password')
        encoded_credentials = encode_credentials(username, password)

        session['encoded_credentials'] = encoded_credentials

        return redirect("/microa/list_posts")
    
    return render_template('main_page.html')

# Route liste des postes
@app.route('/list_posts', methods=['GET'])
@limiter.limit("20 per minute")
def list_posts():
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microa/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = 'http://wordpress:80/wp-json/wp/v2/posts'
    response = requests.get(url, auth=(username, password))
    posts = response.json()
    return render_template('list_posts.html', posts=posts)

# Route édition de postes
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def edit_post(post_id):
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microa/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        url = f'http://wordpress:80/wp-json/wp/v2/posts/{post_id}'
        data = {
            'title': title,
            'content': content
        }
        response = requests.put(url, json=data, auth=(username, password))
        if response.status_code == 200:
            return redirect("/microa/list_posts")
    
    url = f'http://wordpress:80/wp-json/wp/v2/posts/{post_id}'
    response = requests.get(url, auth=(username, password))
    post = response.json()
    return render_template('edit_post.html', post=post, post_id=post_id)

# Route suppression de postes
@app.route('/delete_post/<int:post_id>', methods=['GET'])
@limiter.limit("20 per minute")
def delete_post(post_id):
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microa/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = f'http://wordpress:80/wp-json/wp/v2/posts/{post_id}'
    response = requests.delete(url, auth=(username, password))
    return redirect("/microa/list_posts")

# Route création de postes
@app.route('/create_post', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def create_post():
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microa/")

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        username = request.form.get('username')
        password = request.form.get('password')

        credentials = session.get('encoded_credentials')

        url = 'http://wordpress:80/wp-json/wp/v2/posts'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}'
        }
        data = {
            'title': title,
            'content': content,
            'status': 'publish'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            return redirect("/microa/list_posts")

    return render_template('create_post.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
