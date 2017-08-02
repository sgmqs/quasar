import json
from .config import config
import oauthlib
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .QuasarWebScraper import Scraper


class NorthstarScraper(Scraper):

    """Class for extracting Northstar data via API."""

    # Define OAuth2 Client ID and Client Secret.
    ns_client = config.ns_client_id
    ns_secret = config.ns_client_secret

    # Create Client Object and Obtain Token
    client = BackendApplicationClient(client_id=ns_client)
    oauth = OAuth2Session(client=client)

    def __init__(self, ns_url='https://profile.dosomething.org'):
        """Set Northstar API with all the retry logic of Quasar Web Scraper."""
        Scraper.__init__(self, ns_url)

    # Note to self, should update this method to check for validity of token,
    # and only refresh when necessary. Something like a simple
    # get().status = 422, then new_token, else, return existing token.
    def getToken(self, path='/v2/auth/token'):
        """Send OAuth request for new or refresh token."""
        new_token = self.oauth.fetch_token(self.url + path,
                                           client_id=self.ns_client,
                                           client_secret=self.ns_secret,
                                           scope='admin')
        return new_token['access_token']

    def get(self, path, query_params=''):
        """Set get method to include OAuth 2 Token for Authorization."""
        auth_headers = {'Authorization': 'Bearer ' + str(self.getToken())}
        response = self.session.get(self.url + path, headers=auth_headers,
                                    params=query_params)
        return response.json()

    def post(self, path, body=[]):
        """Set POST method to include OAuth 2 Token for Authorization.
        Args:
            path (str): Add to base URL defined by init for full URI.
            body (dict): Post data for a request, default none.
        """
        auth_headers = {'Authorization': 'Bearer ' + str(self.getToken())}
        response = self.session.post(self.url + path, headers=auth_headers,
                                     data=body)
        return response.json()

    def process_all_pages(self, path, params, process_fn):
        _params = {'limit': 100, 'pagination': 'cursor'}
        _params.update(params)

        _next = True
        current = 1
        while _next is True:
            _params['page'] = current
            response = self.get(path, _params)
            process_fn(current, response)
            current += 1
            if response['meta']['cursor']['next'] is None:
                _next = False
