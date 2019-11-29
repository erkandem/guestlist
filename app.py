import base64
import json
import threading
import urllib
import flask
import requests
from logmod import app_logger
from config import guestoo

DUMMY = {
    'firstName': 'Default',
    'lastName': 'Placeholder',
    'status': 'led led-yellow'
}


def tob64(to_encode):
    return base64.b64encode(
        to_encode.encode('utf-8')
    ).decode('utf-8')


def login():
    credentials_str = f'{guestoo["LOGIN_USER_NAME"]}:{guestoo["LOGIN_SECRET"]}'
    credentials = tob64(credentials_str)
    request_header = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    form_data = {'grant_type': 'client_credentials', 'scope': 'cp'}
    form_data_encoded = urllib.parse.urlencode(form_data)
    response = requests.post(
        guestoo['TOKEN_URL'],
        data=form_data_encoded,
        headers=request_header)
    if response.status_code == 200:
        data = response.json()
        auth_header = {"authorization": f"Bearer {data['access_token']}"}
        guestoo['auth_header'] = auth_header
        app_logger.info(json.dumps({'msg': 'logged in'}))
        return 200
    elif response.status_code == 400:
        app_logger.error(json.dumps({'msg': 'logged failed - bad request'}))
        return 400
    elif response.status_code == 401:
        app_logger.error(json.dumps({'msg': 'logged failed - unauthorized'}))
        return 401
    elif response.status_code == 500:
        app_logger.error(json.dumps({'msg': 'logged failed - server side error'}))
        return 500
    return -1


def start_cron_thread():
    from cron import cron_main
    p = threading.Thread(target=cron_main)
    p.start()
    app_logger.info(json.dumps({'msg': 'started cron thread'}))


def app_factory():
    local_app = flask.Flask("Gästeliste")
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
        'firstName': 'Something',
        'lastName':  'Wrong',
    }
    if response.status_code == 200:
        guests_data = response.json()
        if len(guests_data) > 0:
            guests = [{
                'firstName': elm['firstName'],
                'lastName':  elm['lastName']
            } for elm in guests_data]
        else:
            app_logger.info('No guests listed yet - returning dummy')
            return DUMMY
    else:
        app_logger.error('Could not fetch event specify guests (status!= 200). Returning Dummy')
    return guests


def evaluate_status2led(elm):
    """
    adapter between color rendered by `led.css` and
    statuses returned by `guestoo`

    color-space: ['red', 'orange', 'yellow', 'green', 'blue']
    status-space: ['INVITED', 'OPEN', 'DECLINED', 'CONFIRMED', 'APPEARED']
    """
    guest_status = elm['events'][0]['status']
    if guest_status == 'CONFIRMED':
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
            'id': guestoo['EVENT_ID'],
            'status': ['INVITED', 'OPEN', 'DECLINED', 'CONFIRMED', 'APPEARED']
        }
    }
    response = requests.post(url, json=body, headers=headers)
    guests = {
        'firstName': 'Something',
        'lastName':  'Wrong',
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
        else:
            app_logger.info('No event specifuc guests listed yet - returning dummy')
            return DUMMY
    else:
        app_logger.error('Could not fetch event specify guests (status!= 200). Returning Dummy')
    return guests


app = app_factory()


@app.route('/', methods=['GET'])
def index_route():
    guests = get_event_specific_guests()
    return flask.render_template('index_template.html', guests=guests)


@app.route(f'/{guestoo["REFRESH_URI"]}', methods=['POST'])
def refresh_login():
    status = login()
    return ' ', status


if __name__ == "__main__":
    app.run()

