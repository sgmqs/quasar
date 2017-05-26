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


    def full_backfil(self):
        final_page = self.rogueExtract.get_total_pages()
        current_page = 1
        

    def insert_record(self):
        """Put sanitized record into Blade DB."""
        print(type(self._get_extract_page(1,40)))

    def _get_extract_page(self, page, limit):
        roguePage = self.rogueExtract.get_activity(page, limit)
        return roguePage

    def _transform_records(self, rogue_page):
        """Iterate over page of results from Rogue API and return clean list."""
        parsed_records = []
        for i in rogue_page:
            if i['posts']['data'] is None:
                i['posts']['data']['id'] = ''
                i['posts']['data']['url'] = ''
                i['posts']['data']['caption'] = ''
                i['posts']['data']['status'] = ''
                i['posts']['data']['remote_addr'] = ''
                i['posts']['data']['post_source'] = ''
                i['posts']['data']['created_at'] = ''
                i['posts']['data']['updated_at'] = ''
                parsed_records.append(i)
            else:
                parsed_records.append(i)
        return parsed_records
