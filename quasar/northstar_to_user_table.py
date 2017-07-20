import time
import re
import sys

from .config import config
from .DSNorthstarScraper import NorthstarScraper
from .utils import strip_str
from . import database

"""DS Northstar to Quasar User ETL script.

This ETL scripts scrapes the DoSomething Thor Northstar User API and ETL's the
output to our MySQL Quasar data warehouse.

The script takes an optional argument for what Northstar page result to start
on. This is mostly used to backfill from a certain page, or from the dawn
of time. Otherwise, pagination is stored in an small status tracking table
that gets updated on ingestion loop.

"""


def main():
    start_time = time.time()
    """Keep track of start time of script."""

    # Set pagination variable to be true by default. This
    # will track whether there are any more pages in a
    # result set. If there aren't, will return false.
    nextPage = True

    ca_settings = {'ca': '/home/quasar/rds-combined-ca-bundle.pem'}
    db_opts = {'use_unicode': True, 'charset': 'utf8', 'ssl': ca_settings}
    db, cur = database.connect(db_opts)

    def isInt(s):
        """Check if value is type int and return boolean result.
        Source at http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    if len(sys.argv) == 3:
        if sys.argv[1] == 'prod':
            northstar_env_url = 'https://northstar.dosomething.org'
            db_env = 'users'
        elif sys.argv[1] == 'thor':
            northstar_env_url = 'https://northstar-thor.dosomething.org'
            db_env = 'thor_users'
        else:
            print("Please provide a working Northstar environment: thor/prod.")
            sys.exit(0)
        if sys.argv[2] == 'cont':
            if sys.argv[1] == 'prod':
                cur.execute("SELECT * from quasar_etl_status.northstar_ingestion \
                            WHERE counter_name = 'last_page_scraped'")
                db.commit()
                last_page = cur.fetchall()
                i = last_page[0][1]
            elif sys.argv[1] == 'thor':
                cur.execute("SELECT * from quasar_etl_status.thor_northstar_ingestion \
                           WHERE counter_name = 'last_page_scraped'")
                db.commit()
                last_page = cur.fetchall()
                i = last_page[0][1]
            else:
                print("Can not continue, invalid env specified.")
        elif isInt(sys.argv[2]):
            i = int(sys.argv[2])
        else:
            print("Please input 'cont' to continue backfill or integer value.")
            sys.exit(0)
    else:
        print("Sorry, please specify proper arguments. i.e. env/page")
        sys.exit(0)
    """Determine environment, and page to start from.

    With no arguments, env is set to prod and ingestion begins from last page.
    With 1 argument, env is set to prod and ingestion begins at arg1 page.
    With 2 arguments, env is set to arg1 and ingestion begins at arg2 page.

    """

    # Set environment url for Northstar, prod or thor.
    ns_fetcher = NorthstarScraper(northstar_env_url)

    while nextPage is True:
        current_page = ns_fetcher.getUsers(100, i)
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
                        (strip_str(user['id']),
                         strip_str(user['created_at']),
                         strip_str(user['last_authenticated_at']),
                         strip_str(user['last_accessed_at']),
                         strip_str(user['drupal_id']),
                         strip_str(user['source']),
                         strip_str(user['email']),
                         strip_str(user['mobile']),
                         strip_str(user['birthdate']),
                         strip_str(user['first_name']),
                         strip_str(user['last_name']),
                         strip_str(user['addr_street1']),
                         strip_str(user['addr_street2']),
                         strip_str(user['addr_city']),
                         strip_str(user['addr_state']),
                         strip_str(user['addr_zip']),
                         strip_str(user['country']),
                         strip_str(user['language']),
                         strip_str(user['mobilecommons_id']),
                         strip_str(user['mobilecommons_status']),
                         strip_str(user['source_detail']),
                         strip_str(user['created_at']),
                         strip_str(user['last_authenticated_at']),
                         strip_str(user['last_accessed_at']),
                         strip_str(user['drupal_id']),
                         strip_str(user['source']),
                         strip_str(user['email']),
                         strip_str(user['mobile']),
                         strip_str(user['birthdate']),
                         strip_str(user['first_name']),
                         strip_str(user['last_name']),
                         strip_str(user['addr_street1']),
                         strip_str(user['addr_street2']),
                         strip_str(user['addr_city']),
                         strip_str(user['addr_state']),
                         strip_str(user['addr_zip']),
                         strip_str(user['country']),
                         strip_str(user['language']),
                         strip_str(user['mobilecommons_id']),
                         strip_str(user['mobilecommons_status']),
                         strip_str(user['source_detail'])))
            db.commit()
        nextPage = ns_fetcher.nextPageStatus(100, i)
        if nextPage is True:
            i += 1
            cur.execute("REPLACE INTO quasar_etl_status.northstar_ingestion \
                    (counter_name, counter_value) VALUES(\"last_page_scraped\",\
                    \"{0}\")".format(i))
            db.commit()
        else:
            current_page = ns_fetcher.getUsers(100, i)
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
                            (strip_str(user['id']),
                             strip_str(user['created_at']),
                             strip_str(user['last_authenticated_at']),
                             strip_str(user['last_accessed_at']),
                             strip_str(user['drupal_id']),
                             strip_str(user['source']),
                             strip_str(user['email']),
                             strip_str(user['mobile']),
                             strip_str(user['birthdate']),
                             strip_str(user['first_name']),
                             strip_str(user['last_name']),
                             strip_str(user['addr_street1']),
                             strip_str(user['addr_street2']),
                             strip_str(user['addr_city']),
                             strip_str(user['addr_state']),
                             strip_str(user['addr_zip']),
                             strip_str(user['country']),
                             strip_str(user['language']),
                             strip_str(user['mobilecommons_id']),
                             strip_str(user['mobilecommons_status']),
                             strip_str(user['source_detail']),
                             strip_str(user['created_at']),
                             strip_str(user['last_authenticated_at']),
                             strip_str(user['last_accessed_at']),
                             strip_str(user['drupal_id']),
                             strip_str(user['source']),
                             strip_str(user['email']),
                             strip_str(user['mobile']),
                             strip_str(user['birthdate']),
                             strip_str(user['first_name']),
                             strip_str(user['last_name']),
                             strip_str(user['addr_street1']),
                             strip_str(user['addr_street2']),
                             strip_str(user['addr_city']),
                             strip_str(user['addr_state']),
                             strip_str(user['addr_zip']),
                             strip_str(user['country']),
                             strip_str(user['language']),
                             strip_str(user['mobilecommons_id']),
                             strip_str(user['mobilecommons_status']),
                             strip_str(user['source_detail'])))
                db.commit()

    cur.close()
    db.close()

    end_time = time.time()  # Record when script stopped running.
    duration = end_time - start_time  # Total duration in seconds.
    print('duration: ', duration)

if __name__ == "__main__":
    main()
