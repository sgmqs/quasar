from datetime import datetime as dt
import json
import logging
import sys
import time

import config
import DSHelper as dsh
from DSMySQL import BladeMySQL
from DSRogueWebScraper import RogueScraper

log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)


class RogueEtl:
    """This class ETL's data from DS Rogue API to Blade Data Warehouse.

    The API data is pulled from Rogue Activity API and a series of extracted
    data structures are tested for existence or not.

    The iteration over extracted pages has a hard upper limit that is set at the
    beginning of the ETL run.
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
        get_last_page = dsh.bare_str(self.db.query("SELECT counter_value FROM "
                                                   + self.rogue_progress_table +
                                                   " WHERE counter_name  = \
                                                   'rogue_backfill_page'"))
        if get_last_page is None or int(get_last_page) > 1:
            current_page = int(get_last_page)
        else:
            current_page = 1
        while current_page <= final_page:
            print("Current page is %s." % current_page)
            page_results = self._process_records(
                self._get_activity_page(current_page))
            current_page += 1
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
                self.db.query_str("INSERT INTO " +
                                  self.campaign_activity_table +
                                  " SET northstar_id = %s,\
                                  signup_event_id = %s,\
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
                                  submission_created_at = NULL",
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
                    self.db.query_str("INSERT INTO " +
                                      self.campaign_activity_table +
                                      " SET northstar_id = %s,\
                                      signup_event_id = %s,\
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
