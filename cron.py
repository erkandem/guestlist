from datetime import datetime as dt
import json
import time
import requests
import schedule
from config import guestoo
from logmod import app_logger


def job():
    refresh_url = f'{guestoo["DEPLOYMENT_URL"]}/{guestoo["REFRESH_URI"]}'
    response = requests.get(refresh_url)
    app_logger.info(json.dumps({'msg': f'refresh executed. Status: {response.status_code}'}))


def cron_main():
    schedule.every(guestoo['RELOGIN_HOURS']).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
        app_logger.info(json.dumps({'msg': f'Es ist {dt.now()}'}))


if __name__ == '__main__':
    cron_main()
