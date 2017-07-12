import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class API:
    """ Instantiating a session allows us to re-use the same TCP connection
     for multiple requests to the same host
    """
    def __init__(self, url, retry_total=6, backoff_time=1.9, **defaults):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(defaults['headers'])
        self.session.params.update(defaults['params'])

        retries = Retry(total=retry_total, backoff_factor=backoff_time)
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, path, **args):
        response = self.session.get(''.join((self.url, path)), **args)
        print(response.url)
        return response.json()