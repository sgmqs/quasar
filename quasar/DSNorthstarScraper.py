import json
from .config import config
import oauthlib
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .QuasarWebScraper import Scraper


class NorthstarScraper(Scraper):

    """Class for extracting Northstar data via API."""

    def __init__(self, api_root):
        """Set Northstar API with all the retry logic of Quasar Web Scraper."""
        Scraper.__init__(self, api_root)
        self.auth_headers = self.fetch_auth_headers()

    def fetch_auth_headers(self):
        oauth = OAuth2Session(client=BackendApplicationClient(
            client_id=config.ns_client_id))
        """Send OAuth request for new or refresh token."""
        new_token = oauth.fetch_token(self.url + '/v2/auth/token',
                                      client_id=config.ns_client_id,
                                      client_secret=config.ns_client_secret,
                                      scope='admin')
        return {'Authorization': 'Bearer ' + str(new_token['access_token'])}

    def authenticated(func):
        def _authenticated(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if response.status_code == 401:
                self.auth_headers = self.fetch_auth_headers()
                response = func(self, *args, **kwargs)
            return response
        return _authenticated

    @authenticated
    def get(self, path, query_params=''):
        response = self.session.get(self.url + path, headers=self.auth_headers,
                                    params=query_params)
        return response

    @authenticated
    def post(self, path, body=[]):
        response = self.session.post(self.url + path, headers=self.auth_headers,
                                     data=body)
        return response

    def process_all_pages(self, path, params, process_fn):
        _params = {'limit': 100, 'pagination': 'cursor'}
        _params.update(params)

        i = 1
        if 'page' in params:
            i = params['page']

        _next = True
        while _next is True:
            _params['page'] = i
            response = self.get(path, _params)
            process_fn(i, response)
            i += 1
            if response['meta']['cursor']['next'] is None:
                _next = False
