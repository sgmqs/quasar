from datetime import datetime as dt
import logging
import sys
import time

from .config import config
from .utils import strip_str
from .DSMySQL import BladeMySQL
from .QuasarWebScraper import Scraper

log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)

db = BladeMySQL()
write_table = config.CAMPAIGN_ACTIVITY_TABLE


def full_backfill():
    _backfill()


def backfill_since():
    _backfill(backfill_hours=sys.argv[1])


def _backfill(backfill_hours=None):
    final_page = _get_end_page(backfill_hours)
    current_page = _get_start_page()

    if backfill_hours is not None:
        print("Current backfill hours are %s." % backfill_hours)

    while current_page <= final_page:
        print("Current page: %s of %s" % (current_page, final_page))
        start_time = _now_minus_hours(backfill_hours)
        data = _get_data(current_page, start_time)
        _process_records(data)
        current_page += 1

        if backfill_hours is None:
            _update_progress(current_page)

    try:
        db.create_disconnect()
    except Exception as e:
        print("Exception is %s" % e)
        sys.exit(0)

api_root = ''.join((config.ROGUE_URI, '/api/v2/activity'))
scraper = Scraper(api_root)


def _get(path, page=1, params={}):

    auth_header = {'X-DS-Rogue-API-Key': config.DS_ROGUE_API_KEY}
    default_params = {'page': page, 'limit': 40}
    default_params.update(params)

    response = scraper.get(path, headers=auth_header,
                           query_params=default_params)
    return response.json()


def _get_data(page=1, from_time=None):
    """ Args:
        from_time (str): Date as MM-DD-YYYY HH:MM:SS. If specified, only returns data after this time
    """
    params = {}
    if from_time is not None:
        params = {'filter[updated_at]': from_time}
    return _get('', page, params)['data']


def _get_pages(page=1, from_time=None):
    """ Args:
        from_time (str): Date as MM-DD-YYYY HH:MM:SS. If specified, only returns data after this time
    """
    params = {}
    if from_time is not None:
        params = {'filter[updated_at]': from_time}
    return _get('', page, params)['meta']['pagination']['total_pages']


def _get_start_page():
    table = config.ROGUE_PROGRESS_TABLE
    querystr = ''.join(("SELECT counter_value FROM ", config.ROGUE_PROGRESS_TABLE,
                        " WHERE counter_name = 'rogue_backfill_page'"))

    last_page = strip_str(db.query(querystr))
    if last_page is None or int(last_page) > 1:
        return int(last_page)
    else:
        return 1


def _get_end_page(backfill_hours=None):
    start_time = _now_minus_hours(backfill_hours)
    final_page = _get_pages(from_time=start_time)
    return final_page


def _now_minus_hours(hours):
    """Returns time x hours ago"""
    if hours is None:
        return None
    else:
        start_time = int(time.time()) - (int(hours) * 3600)
        return dt.fromtimestamp(start_time).isoformat()


def _update_progress(page):
    db.query_str("REPLACE INTO " + config.ROGUE_PROGRESS_TABLE +
                 " (counter_name, counter_value) VALUES(%s, %s)",
                 ('rogue_backfill_page', page))


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
                              (strip_str(i['northstar_id']),
                               strip_str(i['signup_id']),
                               strip_str(i['campaign_id']),
                               strip_str(i['campaign_run_id']),
                               strip_str(i['quantity']),
                               strip_str(i['why_participated']),
                               strip_str(i['signup_source']),
                               strip_str(i['created_at']),
                               strip_str(i['updated_at'])))
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
                                  (strip_str(i['northstar_id']),
                                   strip_str(i['signup_id']),
                                   strip_str(i['campaign_id']),
                                   strip_str(i['campaign_run_id']),
                                   strip_str(i['quantity']),
                                   strip_str(i['why_participated']),
                                   strip_str(i['signup_source']),
                                   strip_str(i['created_at']),
                                   strip_str(i['updated_at']),
                                   strip_str(j['id']),
                                   strip_str(j['media']['url']),
                                   strip_str(j['media']['caption']),
                                   strip_str(j['status']),
                                   strip_str(j['remote_addr']),
                                   strip_str(j['source']),
                                   strip_str(j['created_at']),
                                   strip_str(j['updated_at'])))
