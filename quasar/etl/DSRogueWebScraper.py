import config
from .QuasarWebScraper import Scraper


class RogueScraper(Scraper):
    """Class for extracting Rogue data via API."""

    # Set Rogue API key.
    rogue_api_key = config.DS_ROGUE_API_KEY

    def __init__(self, ds_rogue_url=config.ROGUE_URI):
        """Set Rogue API with all retry goodness of Quasar Web Scraper."""
        rogue_url = ds_rogue_url
        Scraper.__init__(self, rogue_url)

    def get(self, path, query_params=''):
        """Set get method to use Rogue API Key."""
        auth_header = {'X-DS-Rogue-API-Key': self.rogue_api_key}
        response = self.session.get(self.url + path,
                                    headers=auth_header,
                                    params=query_params)
        return response.json()

    def get_activity(self, page=1, limit=40):
        """Get activity from Rogue API with page and limit.

        Args:
            page_number (int): Page number to send to request, default 1.
            limit (int): Total responses to send per page, default 40.
        """
        activity_response = self.get('/api/v2/activity',
                                     {'page': page, 'limit': limit})
        return(activity_response['data'])

    def get_latest_activity(self, time_since, page=1, limit=40):
        """Get activity from Rogue API since designated timestamp to now.

        Args:
            time_since (str): Date in format MM-DD-YYYY HH:MM:SS
            page_number (int): Page number to send to request, default 1.
            limit (int): Total responses to send per page, default 40.
        """
        params = ('?page=' + str(page) + '&limit=' + str(limit) +
                  '&filter[updated_at]=' + str(time_since))
        activity_response = self.get('/api/v2/activity' + params)
        return(activity_response['data'])

    def get_total_pages(self, page=1, limit=40):
        """Get total pages from Rogue API with page and limit.

        Args:
            page_number (int): Page number to send to request, default 1.
            limit (int): Total responses to per page, default 40.
            """
        page_response = self.get('/api/v2/activity',
                                 {'page': page, 'limit': limit})
        return(page_response['meta']['pagination']['total_pages'])

    def get_total_pages_latest(self, time_since, page=1, limit=40):
        """Get total pages from Rogue API with backfill hours limit.

        Args:
            time_since (str): Date in format MM-DD-YYYY HH:MM:SS
            page_number (int): Page number to send to request, default 1.
            limit (int): Total responses to send per page, default 40.
        """
        params = ('?page=' + str(page) + '&limit=' + str(limit) +
                  '&filter[updated_at]=' + str(time_since))
        page_response = self.get('/api/v2/activity' + params)
        return(page_response['meta']['pagination']['total_pages'])
