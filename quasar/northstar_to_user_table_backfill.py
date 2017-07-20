from datetime import datetime as dt
import re
import sys
import time

from . import database

from .config import config
from .DSNorthstarScraper import NorthstarScraper

"""DS Northstar to Quasar User ETL script.

This ETL scripts scrapes the DoSomething Thor Northstar User API and ETL's the
output to our MySQL Quasar data warehouse.

The script takes an optional argument for what Northstar page result to start
on. This is mostly used to backfill from a certain page, or from the dawn
of time. Otherwise, pagination is stored in an small status tracking table
that gets updated on ingestion loop.

"""


def isInt(s):
    """Check if value is type int and return boolean result.
    Source at http://stackoverflow.com/questions/1265665/python-check-
                     if-a-string-represents-an-int-without-using-try-except
    """
    try:
        int(s)
        return True
    except ValueError:
        return False



def to_string(base_value):
    """Converts to string and replaces None values with empty values."""
    if base_value is None:
        return None
    else:
        base_string = str(base_value)
        strip_special_chars = re.sub(r'[()<>/"\'\\]', '', base_string)
        return str(strip_special_chars)


def main():
    def updateCreatedSince(formatted_time):
        """Grab all new NS users created since backfill time."""
        nextPage = ns_fetcher.nextPageStatusCreatedSince(formatted_time)
        i = 1
        while nextPage is True:
            current_page = ns_fetcher.getUsersCreatedSince(formatted_time, 100, i)
            _process_records(current_page)
            nextPage = ns_fetcher.nextPageStatusCreatedSince(formatted_time,
                                                             100, i)
            if nextPage is True:
                i += 1
            else:
                current_page = ns_fetcher.getUsersCreatedSince(formatted_time,
                                                               100, i)
                _process_records(current_page)


    def updateUpdatedSince(formatted_time):
        """Grab all new NS users created since backfill time."""
        nextPage = ns_fetcher.nextPageStatusUpdatedSince(formatted_time)
        i = 1
        while nextPage is True:
            current_page = ns_fetcher.getUsersUpdatedSince(formatted_time, 100, i)
            _process_records(current_page)
            nextPage = ns_fetcher.nextPageStatusUpdatedSince(formatted_time,
                                                             100, i)
            if nextPage is True:
                i += 1
            else:
                current_page = ns_fetcher.getUsersUpdatedSince(formatted_time,
                                                               100, i)
                _process_records(current_page)


    def _process_records(current_page):
        """Process Northstar API JSON to user table records."""
        for user in current_page:
            cur.execute("INSERT INTO quasar.users (northstar_id,\
                        northstar_created_at_timestamp,\
                        last_logged_in, last_accessed, drupal_uid,\
                        northstar_id_source_name,\
                        email, mobile, birthdate,\
                        first_name, last_name,\
                        addr_street1, addr_street2,\
                        addr_city, addr_state,\
                        addr_zip, country, language,\
                        agg_id, cgg_id,\
                        moco_commons_profile_id,\
                        moco_current_status,\
                        moco_source_detail)\
                        VALUES(%s,%s,%s,%s,%s,%s,\
                        %s,%s,%s,%s,\
                        %s,%s,%s,%s,\
                        %s,%s,%s,%s,\
                        NULL,NULL,%s,%s,%s)\
                        ON DUPLICATE KEY UPDATE \
                        northstar_created_at_timestamp = %s,\
                        last_logged_in = %s,\
                        last_accessed = %s, drupal_uid = %s,\
                        northstar_id_source_name = %s,\
                        email = %s, mobile = %s, birthdate = %s,\
                        first_name = %s, last_name = %s,\
                        addr_street1 = %s, addr_street2 = %s,\
                        addr_city = %s, addr_state = %s,\
                        addr_zip = %s, country = %s, language = %s,\
                        agg_id = NULL, cgg_id = NULL,\
                        moco_commons_profile_id = %s,\
                        moco_current_status = %s,\
                        moco_source_detail = %s",
                        (to_string(user['id']),
                         to_string(user['created_at']),
                         to_string(user['last_authenticated_at']),
                         to_string(user['last_accessed_at']),
                         to_string(user['drupal_id']),
                         to_string(user['source']),
                         to_string(user['email']),
                         to_string(user['mobile']),
                         to_string(user['birthdate']),
                         to_string(user['first_name']),
                         to_string(user['last_name']),
                         to_string(user['addr_street1']),
                         to_string(user['addr_street2']),
                         to_string(user['addr_city']),
                         to_string(user['addr_state']),
                         to_string(user['addr_zip']),
                         to_string(user['country']),
                         to_string(user['language']),
                         to_string(user['mobilecommons_id']),
                         to_string(user['mobilecommons_status']),
                         to_string(user['source_detail']),
                         to_string(user['created_at']),
                         to_string(user['last_authenticated_at']),
                         to_string(user['last_accessed_at']),
                         to_string(user['drupal_id']),
                         to_string(user['source']),
                         to_string(user['email']),
                         to_string(user['mobile']),
                         to_string(user['birthdate']),
                         to_string(user['first_name']),
                         to_string(user['last_name']),
                         to_string(user['addr_street1']),
                         to_string(user['addr_street2']),
                         to_string(user['addr_city']),
                         to_string(user['addr_state']),
                         to_string(user['addr_zip']),
                         to_string(user['country']),
                         to_string(user['language']),
                         to_string(user['mobilecommons_id']),
                         to_string(user['mobilecommons_status']),
                         to_string(user['source_detail'])))
            db.commit()


    start_time = time.time()
    """Keep track of start time of script."""


    # Set pagination variable to be true by default. This
    # will track whether there are any more pages in a
    # result set. If there aren't, will return false.
    nextPage = True

    # ca_settings = {'ca': '/home/quasar/rds-combined-ca-bundle.pem'}
    # db_opts = {'use_unicode': True, 'charset': 'utf8', 'ssl': ca_settings}
    db_opts = {}
    db, cur = database.connect(db_opts)

    if len(sys.argv) == 2:
        if isInt(sys.argv[1]):
            backfill_hours = sys.argv[1]
    else:
        print("Sorry, please specify single argument of hours to backfill!")
        sys.exit(0)
    """Determine backfill hours and set for updated and created backfills."""

    # Create NS Scraper and format backfill period to ISO8601.
    ns_fetcher = NorthstarScraper('https://northstar.dosomething.org')
    backfill_since = int(time.time()) - (int(backfill_hours) * 3600)
    backfill_formatted_time = dt.fromtimestamp(backfill_since).isoformat()

    updateCreatedSince(backfill_formatted_time)
    updateUpdatedSince(backfill_formatted_time)

    cur.close()
    db.close()

    end_time = time.time()  # Record when script stopped running.
    duration = end_time - start_time  # Total duration in seconds.
    print('duration: ', duration)


if __name__ == "__main__":
    main()