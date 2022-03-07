import requests


class BadStatusError(Exception):
    pass


class Api_ext:
    METHOD = 'GET'
    BASE_URL = 'http://127.0.0.1:8000/'

    def call(self, **kwargs) -> dict:
        kwargs['method'] = kwargs.get('method', self.METHOD)
        kwargs['url'] = self.BASE_URL + kwargs.get('url', '')

        req = requests.request(**kwargs)
        if req.status_code != 200:
            print('ERROR status_code', req.status_code)
            raise BadStatusError

        return req.json()
