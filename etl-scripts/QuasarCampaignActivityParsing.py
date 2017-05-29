from datetime import datetime
import json
import logging

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
        self.rogueLoad = BladeMySQL()
        self.campaign_activity_table = config.CAMPAIGN_ACTIVITY_TABLE

    def full_backfill(self):
        """Run or resume full backfill of Campaign Activity from Rogue API."""
        self.rogueLoad.create_connection()
        final_page = self.rogueExtract.get_total_pages()
        current_page = 1
        while current_page <= final_page:
            print("Current page is %s." % current_page)
            page_results = self._process_records(
                self._get_activity_page(current_page))
            current_page += 1
        self.rogueLoad.create_disconnect()

    def insert_record(self):
        """Put sanitized record into Blade DB."""
        print(type(self._get_extract_page(1,40)))

    def _get_activity_page(self, page, limit=40):
        """Get a paginated response from Rogue API."""
        roguePage = self.rogueExtract.get_activity(page, limit)
        return roguePage

    def _process_records(self, rogue_page):
        """Iterate over page of results ."""
        for i in rogue_page:
            if i['posts']['data'] == []:
                query = """INSERT INTO {0} SET northstar_id = \"{1}\",
                           signup_event_id = \"{2}\",
                           campaign_id = {3},
                           campaign_run_id = {4},
                           quantity = {5},
                           why_participated = \"{6}\",
                           signup_source = \"{7}\",
                           signup_created_at = {8},
                           signup_updated_at = {9},
                           post_id = {10},
                           url = {11},
                           caption = {12},
                           status = {13},
                           remote_addr = {14},
                           post_source = {15},
                           submission_created_at = {16},
                           submission_updated_at = {17}
                           """.format(self.campaign_activity_table,
                                      dsh.bare_str(i['northstar_id']),
                                      dsh.bare_str(i['signup_id']),
                                      dsh.bare_str(i['campaign_id']),
                                      dsh.bare_str(i['campaign_run_id']),
                                      dsh.bare_str(i['quantity']),
                                      dsh.bare_str(i['why_participated']),
                                      dsh.bare_str(i['signup_source']),
                                      dsh.bare_str(i['created_at']),
                                      dsh.bare_str(i['updated_at']),
                                      None, None, None, None, None, None,
                                      None, None)
                self.rogueLoad.mysql_query(query)
            else:
                for j in i['posts']['data']:
                    query = """INSERT INTO {0} SET northstar_id = \"{1}\",
                            signup_event_id = \"{2}\",
                            campaign_id = {3},
                            campaign_run_id = {4},
                            quantity = {5},
                            why_participated = \"{6}\",
                            signup_source = \"{7}\",
                            signup_created_at = {8},
                            signup_updated_at = {9},
                            post_id = {10},
                            url = \"{11}\",
                            caption = \"{12}\",
                            status = \"{13}\",
                            remote_addr = \"{14}\",
                            post_source = \"{15}\",
                            submission_created_at = {16},
                            submission_updated_at = {17}
                            """.format(self.campaign_activity_table,
                                       dsh.bare_str(i['northstar_id']),
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
                                       dsh.bare_str(j['updated_at']))
                    self.rogueLoad.mysql_query(query)
