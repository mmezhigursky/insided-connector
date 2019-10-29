import os
import requests
import time
import json
from datetime import datetime
import credential


proxy = credential.proxy

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


CLIENT_ID = credential.CLIENT_ID

CLIENT_SECRET = credential.CLIENT_SECRET


class Insided (object):    
    
    DEFAULT_ENDPOINT ='https://api2-eu-west-1.insided.com'

    DATE = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())

    SCOPE = 'read'
    
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',}

    def __init__(self, CLIENT_ID, CLIENT_SECRET, endpoint=DEFAULT_ENDPOINT, scope = SCOPE):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.endpoint = endpoint
        self.session = requests.Session()
        self.scope = scope
        

    def request(self, method, query={}):
        try:

            headers = {
            'Authorization': 'Bearer ' + self._tokenBuilder(),
            'Content-Type': 'application/json'
            }

            request = self.session.get(
                self.endpoint + method,
                headers = headers,
                params=query
            )
            response = request.json()
        except Exception as e:
            print(str(e))
            
        return response



    def _tokenBuilder(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',}
        params = {
                'grant_type':'client_credentials',
                'client_id':self.client_id,
                'client_secret':self.client_secret ,
                'scope': self.scope
                }
        ENDPOINT = self.endpoint + '/oauth2/access_token'
        response = requests.post(ENDPOINT, headers= headers, params=params)
        
        return  response.json()['access_token']


    def get_all_users(self, data_from, data_to):
        
        self.data_from = datetime.strptime(data_from,'%Y-%m-%d')
        self.data_to =  datetime.strptime(data_to,'%Y-%m-%d')

        params = {
            'filter[joindate][from]':int(self.data_from.timestamp()),
            'filter[joindate][to]':int(self.data_to.timestamp())
            }

        return self.request('/user', params)

    def get_registered_user (self, data_from, data_to):
        
        self.data_from = datetime.strptime(data_from,'%Y-%m-%d')
        self.data_to =  datetime.strptime(data_to,'%Y-%m-%d')

        params = {
            'filter[roles]':'roles.registered',
            'filter[joindate][from]':int(self.data_from.timestamp()),
            'filter[joindate][to]':int(self.data_to.timestamp())
            }

        return self.request('/user/activity', params)

instance_new = Insided(CLIENT_ID, CLIENT_SECRET)
print(instance_new.get_registered_user('2019-04-01', '2019-07-31'))

