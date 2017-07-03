from datetime import datetime as dt
import logging
import sys
import time

from .config import config
from . import DSHelper as dsh
from .DSMySQL import BladeMySQL
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


class RogueEtl:
    """This class ETL's data from DS Rogue API to Blade Data Warehouse.

    The API data is pulled from Rogue Activity API and a series of extracted
    data structures are tested for existence or not.

    The iteration over extracted pages has a hard upper limit that is set at
    the beginning of the ETL run.
    """

    def __init__(self):
        """Setup Rogue Scraper and MySQL connection."""
        self.rogueExtract = RogueScraper()
        self.db = BladeMySQL()
        self.campaign_activity_table = config.CAMPAIGN_ACTIVITY_TABLE
        self.rogue_progress_table = config.ROGUE_PROGRESS_TABLE

    def full_backfill(self):
        """Run or resume full backfill of Campaign Activity from Rogue API."""
        final_page = self.rogueExtract.get_total_pages()
        last_page = dsh.bare_str(self.db.query("SELECT counter_value FROM " +
                                               self.rogue_progress_table +
                                               " WHERE counter_name  = \
                                                'rogue_backfill_page'"))
        if last_page is None or int(last_page) > 1:
            current_page = int(last_page)
        else:
            current_page = 1
        while current_page <= final_page:
            print("Current page: %s of %s" % (current_page, final_page))
            self._process_records(self._get_activity_page(current_page))
            current_page += 1
            self.db.query_str("REPLACE INTO " + self.rogue_progress_table +
                              " (counter_name, counter_value) VALUES(%s, %s)",
                              ('rogue_backfill_page', current_page))
        print("Reached final page in full backfill: %s" % final_page)
        self.db.create_disconnect()

    def backfill_since(self, backfill_hours):
        """Update activity from now - backfill_hours as backfill."""
        backfill_since = int(time.time()) - (int(backfill_hours) * 3600)
        formatted_time = dt.fromtimestamp(backfill_since).isoformat()
        final_page = self.rogueExtract.get_total_pages_latest(formatted_time)
        current_page = 1
        print("Current backfill hours are %s." % backfill_hours)
        while current_page <= final_page:
            print("Current page is %s." % current_page)
            self._process_records(self._get_updated_page(formatted_time,
                                                         current_page))
            current_page += 1
        try:
            self.db.create_disconnect()
        except Exception as e:
            print("Exception is %s" % e)
            print("No records in this backfill period.")
            sys.exit(0)

    def insert_record(self):
        """Put sanitized record into Blade DB."""
        print(type(self._get_extract_page(1, 40)))

    def _get_activity_page(self, page, limit=40):
        """Get a paginated response from Rogue API."""
        roguePage = self.rogueExtract.get_activity(page, limit)
        return roguePage

    def _get_updated_page(self, time_since, page, limit=40):
        """Get a paginated response from updated_at Rogue API endpoint."""
        roguePage = self.rogueExtract.get_latest_activity(time_since, page,
                                                          limit)
        return roguePage

    def _process_records(self, rogue_page):
        """Iterate over page of results and load into Blade DB."""
        for i in rogue_page:
            if i['posts']['data'] == []:
                self.db.query_str("REPLACE INTO " +
                                  self.campaign_activity_table +
                                  " SET northstar_id = %s,\
                                  signup_id = %s,\
                                  campaign_id = %s,\
                                  campaign_run_id = %s,\
                                  quantity = %s,\
                                  why_participated = %s,\
                                  signup_source = %s,\
                                  signup_created_at = %s,\
                                  signup_updated_at = %s,\
                                  post_id = NULL,\
                                  url = NULL,\
                                  caption = NULL,\
                                  status = NULL,\
                                  remote_addr = NULL,\
                                  post_source = NULL,\
                                  submission_created_at = ''",
                                  (dsh.bare_str(i['northstar_id']),
                                   dsh.bare_str(i['signup_id']),
                                   dsh.bare_str(i['campaign_id']),
                                   dsh.bare_str(i['campaign_run_id']),
                                   dsh.bare_str(i['quantity']),
                                   dsh.bare_str(i['why_participated']),
                                   dsh.bare_str(i['signup_source']),
                                   dsh.bare_str(i['created_at']),
                                   dsh.bare_str(i['updated_at'])))
            else:
                for j in i['posts']['data']:
                    self.db.query_str("REPLACE INTO " +
                                      self.campaign_activity_table +
                                      " SET northstar_id = %s,\
                                      signup_id = %s,\
                                      campaign_id = %s,\
                                      campaign_run_id = %s,\
                                      quantity = %s,\
                                      why_participated = %s,\
                                      signup_source = %s,\
                                      signup_created_at = %s,\
                                      signup_updated_at = %s,\
                                      post_id = %s,\
                                      url = %s,\
                                      caption = %s,\
                                      status = %s,\
                                      remote_addr = %s,\
                                      post_source = %s,\
                                      submission_created_at = %s,\
                                      submission_updated_at = %s",
                                      (dsh.bare_str(i['northstar_id']),
                                       dsh.bare_str(i['signup_id']),
                                       dsh.bare_str(i['campaign_id']),
                                       dsh.bare_str(i['campaign_run_id']),
                                       dsh.bare_str(i['quantity']),
                                       dsh.bare_str(i['why_participated']),
                                       dsh.bare_str(i['signup_source']),
                                       dsh.bare_str(i['created_at']),
                                       dsh.bare_str(i['updated_at']),
                                       dsh.bare_str(j['id']),
                                       dsh.bare_str(j['media']['url']),
                                       dsh.bare_str(j['media']['caption']),
                                       dsh.bare_str(j['status']),
                                       dsh.bare_str(j['remote_addr']),
                                       dsh.bare_str(j['source']),
                                       dsh.bare_str(j['created_at']),
                                       dsh.bare_str(j['updated_at'])))


log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
etl = RogueEtl()

def full_backfill():
    etl.full_backfill()

def backfill_since():
    etl.backfill_since(sys.argv[1])