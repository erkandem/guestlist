import base64
import json
import threading
import urllib
import flask
import requests
from logmod import app_logger
from config import guestoo, REFRESH_URI


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


def start_cron_thread():
    from cron import cron_main
    p = threading.Thread(target=cron_main)
    p.start()
    app_logger.info(json.dumps({'msg': 'started cron thread'}))


def app_factory():
    local_app = flask.Flask("Gäschtelischte")
    local_app.guestoo = guestoo
    login()
    start_cron_thread()
    return local_app


def get_guests():
    headers = {
        'accept': 'application/json',
        **guestoo['auth_header']
    }
    url = guestoo['GUESTS_URL']
    response = requests.get(url, headers=headers)
    guests = {
        'firstName': 'Someting',
        'lastName':  'Wong',
    }
    if response.status_code == 200:
        guests_data = response.json()
        if len(guests_data) > 0:
            guests = [{
                'firstName': elm['firstName'],
                'lastName':  elm['lastName']
            } for elm in guests_data]
    return guests


def evaluate_status2led(elm):
    if elm['events'][0]['status'] == 'CONFIRMED':
        status = 'led led-green'
    else:
        status = 'led led-yellow'
    return status


def get_event_specific_guests():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        **guestoo['auth_header']
    }
    url = guestoo['DETAILED_GUESTS_URL']
    body = {
        'event': {
            '"id': guestoo['EVENT_ID'],
            'status': ['INVITED', 'OPEN', 'DECLINED', 'CONFIRMED', 'APPEARED']
        }
    }
    response = requests.post(url, json=body, headers=headers)
    guests = {
        'firstName': 'Someting',
        'lastName':  'Wong',
        'status': 'led led-red'
    }
    if response.status_code == 200:
        guests_data = response.json()
        if len(guests_data) > 0:
            guests = [{
                'firstName': elm['firstName'],
                'lastName':  elm['lastName'],
                'status': evaluate_status2led(elm)
            } for elm in guests_data]
    return guests


app = app_factory()


@app.route('/', methods=['GET'])
def index_route():
    guests = get_event_specific_guests()
    return flask.render_template('index_temp.html', guests=guests)


@app.route(f'/{REFRESH_URI}', methods=['POST'])
def refresh_login():
    status = login()
    return ' ', status


if __name__ == "__main__":
    app.run()

