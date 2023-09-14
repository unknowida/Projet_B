from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import requests
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # secret key config
app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE') # stockage de la session
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

        session['encoded_credentials'] = encoded_credentials

        return redirect("/microb/list_pages")
    
    return render_template('pages.html')

@app.route('/list_pages', methods=['GET'])
@limiter.limit("20 per minute")
def list_pages():
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microb/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = 'http://wordpress:80/wp-json/wp/v2/pages'
    response = requests.get(url, auth=(username, password))
    pages = response.json()
    return render_template('list_pages.html', pages=pages, encoded_credentials=encoded_credentials)

@app.route('/edit_page/<int:page_id>', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def edit_page(page_id):
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microb/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        url = f'http://wordpress:80/wp-json/wp/v2/pages/{page_id}'
        data = {
            'title': title,
            'content': content
        }
        response = requests.put(url, json=data, auth=(username, password))
        if response.status_code == 200:
            return redirect("/microb/list_pages")
    
    url = f'http://wordpress:80/wp-json/wp/v2/pages/{page_id}'
    response = requests.get(url, auth=(username, password))
    page = response.json()
    return render_template('edit_page.html', page=page, page_id=page_id)

@app.route('/delete_page/<int:page_id>', methods=['GET'])
@limiter.limit("20 per minute")
def delete_page(page_id):
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microb/")

    credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
    username, password = credentials[0], credentials[1]

    url = f'http://wordpress:80/wp-json/wp/v2/pages/{page_id}'
    response = requests.delete(url, auth=(username, password))
    return redirect("/microb/list_pages")

@app.route('/create_page', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def create_page():
    encoded_credentials = session.get('encoded_credentials')

    if encoded_credentials is None:
        return redirect("/microb/")

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        credentials = session.get('encoded_credentials')

        url = 'http://wordpress:80/wp-json/wp/v2/pages'
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
            return redirect("/microb/list_pages")

    return render_template('create_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
