from datetime import datetime
import logging

import config
import DSHelper
# from DSMySQL import BladeMySQL
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
        # rogueLoad = BladeMySQL(config.CAMPAIGN_ACTIVITY_TABLE)


    def full_backfill(self):
        final_page = self.rogueExtract.get_total_pages()
        current_page = 1
        while current_page <= final_page:
            print("Current page is %s." % current_page)
            page_results = self._transform_records(
                self._get_activity_page(current_page))
            current_page += 1


    def insert_record(self):
        """Put sanitized record into Blade DB."""
        print(type(self._get_extract_page(1,40)))

    def _get_activity_page(self, page, limit=40):
        roguePage = self.rogueExtract.get_activity(page, limit)
        return roguePage

    def _transform_records(self, rogue_page):
        """Iterate over page of results from Rogue API and return clean list."""
        parsed_records = []
        for i in rogue_page:
            if i['posts']['data'] == []:
                i['posts']['data'] = {'id': '', 'status': '',
                                      'media': {'caption': '', 'url': ''},
                                      'remote_addr': '','post_source': '',
                                      'created_at': '', 'updated_at': ''}
                parsed_records.append(i)
            else:
                parsed_records.append(i)
        return parsed_records
