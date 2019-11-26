import dotenv
import base64
import requests
import flask
from config import guestoo, REFRESH_URI
import multiprocessing
import urllib
from logmod import app_logger
import json


def tob64(to_encode):
    return base64.b64encode(
        to_encode.encode('utf-8')
    ).decode('utf-8')


def login():
    user = guestoo['LOGIN_USER_NAME']
    pw = guestoo['LOGIN_SECRET']
    credentials = tob64(f'{user}:{pw}')
    request_header = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    form_data = {'grant_type': 'client_credentials', 'scope': 'cp'}
    data = urllib.parse.urlencode(form_data)
    response = requests.post(
        guestoo['TOKEN_URL'],
        data=data,
        headers=request_header)
    if response.status_code == 200:
        data = response.json()
        auth_header = {"authorization": f"Bearer {data['access_token']}"}
        guestoo['auth_header'] = auth_header
        app_logger.info(json.dumps({'msg': 'logged in'}))
        return 200
    return 500


def start_cron_process():
    from cron import cron_main
    p = multiprocessing.Process(target=cron_main)
    p.start()
    app_logger.info(json.dumps({'msg': 'started cron'}))


def app_factory():
    app = flask.Flask("Gäschtelischte")
    app.guestoo = guestoo
    login()
    start_cron_process()
    return app


def get_cleaned_users():
    header = {
        "accept": "application/json",
        **guestoo['auth_header']
    }
    response = requests.get(guestoo['GUESTS_URL'], headers=header)
    guests = {
        "firstName": "Someting",
        "lastName":  "Wong",
    }
    if response.status_code == 200:
        guests_data = response.json()
        if len(guests_data) > 0:
            guests = [{
                "firstName": elm["firstName"],
                "lastName":  elm["lastName"],
            } for elm in guests_data]
    return guests


app = app_factory()


@app.route('/', methods=['GET'])
def index():
    guests = get_cleaned_users()
    return flask.render_template('index_temp.html', guests=guests)


@app.route('/' + REFRESH_URI, methods=['POST'])
def refresh_login():
    status = login()
    return ' ', status


if __name__ == "__main__":
    app.run()

