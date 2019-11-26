import schedule
import time
import requests
from config import REFRESH_URI
from datetime import datetime as dt
from logmod import app_logger
import json


def job():
    refresh_url = f'localhost:5000/{REFRESH_URI}'
    response = requests.get(refresh_url)
    app_logger.info(json.dumps({'msg': f'refresh executed. Status: {response.status_code}'}))


def cron_main():
    schedule.every(10).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
        app_logger.info(json.dumps({'msg': f'es isch {dt.now()}'}))


if __name__ == '__main__':
    cron_main()
