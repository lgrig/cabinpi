import pandas as pd
from datetime import datetime
import pytz
import json
import requests
from requests.auth import HTTPBasicAuth
import shutil
import http.cookiejar as cookielib
import time
from tools.connection import Connection

class EnergyUsage:
    def __init__(self):
        self.config = Connection().config['pge']

    def start_session(self):
        jar = cookielib.CookieJar()
        with requests.Session() as s:
            payload = {
                'username': self.config['username'],
                'password': self.config['password'],
                'globalsync': True,
                'type': 'LOGIN'}
            s.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                         'Content-Type': 'application/json',
                         'Accept': '*/*',
                         'Connection': 'keep-alive',
                         'Accept-Encoding': 'gzip, deflate, br',
                         'Content-Length': '88'}
            post = s.options('https://apim.pge.com/login?ts={}'.format(int(time.time())), data=payload)
        return post

    def get_energy_data(self, startdate=None, enddate=None):
        session = self.start_session()
        local_filename = 'pge_' + enddate + '.csv'
        request_url = "https://pge.opower.com/ei/app/api/usage_export/download?format=csv&startDate={startdate}&endDate={enddate}"
        request_url = request_url.format(startdate=startdate, enddate=enddate)
        r = session.get(request_url, stream=True)
        if r.status_code == 200:
            with open('./' + local_filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        return local_filename

    @staticmethod
    def measure():
        now = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone("US/Pacific")).strftime("%Y-%m-%d %H:%M:%S")
        try:
            return json.dumps({
                'random_number': {
                    'task': 'gen_random_number',
                    'status': 'success',
                    'value_numeric': num,
                    'value_enum': None,
                    'timestamp': now}
                })

        except BaseException as err:
            return json.dumps({
                'random_number': {
                    'task': 'gen_random_number',
                    'status': 'failure',
                    'value_numeric': None,
                    'value_enum': None,
                    'timestamp': now}
                })
