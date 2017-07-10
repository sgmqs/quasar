import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re
from bs4 import BeautifulSoup
import sys

from .config import config
from . import database


def get(path, payload):
    retries = Retry(total=6, backoff_factor=600)
    req = requests.Session()
    req.mount('https://', HTTPAdapter(max_retries=retries))
    path = ''.join(('https://secure.mcommons.com/api/', path))
    response = requests.get(path, params=payload,
                            auth=(config.mc_user, config.mc_pw))
    return response

def backfill_user_profiles():
    _backfill_user_profiles(sys.argv[1])


def _backfill_user_profiles(backfill_hours):
    db, cur = _connect_db()

    # Time Conversion from Now to ISO 8601 format used by MC
    now = datetime.now()
    now_iso = now.isoformat().replace("-", "").replace(":", "").split(".")
    now_iso = now_iso[0]

    # Break down total time backfill to go based on current execute time of
    # scripts
    origin_time = now - timedelta(hours=int(backfill_hours))
    origin_time_iso = origin_time.isoformat().replace(
        "-", "").replace(":", "").split(".")
    origin_time_iso = origin_time_iso[0]

    print("Backfilling mobile users by " + backfill_hours + " hours.")

    # Set Initial Page and Limit Vars
    limit_num = 300
    page_num = 0

    while limit_num == 300:
        page_num += 1
        # Setup Mobile Commons API Payload and Request

        payload = {'from': origin_time_iso, 'to': now_iso,
                   'limit': '300', 'page': page_num}
        mob_com_api_profile_req = get("profiles", payload)

        # Capture output as BeautifulSoup object, and iterate page till "num"
        # does not equal 300 (default page limit set by script)
        profile_parse = BeautifulSoup(mob_com_api_profile_req.text, 'xml')
        # Set Num of profile for next run-through
        limit_num = int(profile_parse.profiles.get('num'))
        profiles = profile_parse.find_all('profile')

        # Iterate through each profile and insert into DB
        for profile in profiles:
            phone_number = profile.phone_number.text
            created_at = profile.created_at.text.replace(" UTC", "")
            source_type = profile.source.get('type')
            source_name = profile.source.get('name')
            status = profile.status.text
            uid = "NULL"
            if len(phone_number.strip()) == 11 and phone_number.startswith('1'):
                us_phone_number = phone_number[1:11]
            else:
                us_phone_number = "NULL"
            if source_type == "Opt-In Path":
                opt_in_path_id = profile.source.get('id')
            else:
                opt_in_path_id = "NULL"
            insert_profile = "replace into users_and_activities.mobile_user_lookup VALUES ({0}, {1}, {2}, \"{3}\", \"{4}\", \"{5}\", {6}, \"{7}\")".format(
                phone_number, us_phone_number, uid, created_at, source_type, source_name, opt_in_path_id, status)
            cur.execute(insert_profile)
            db.commit()


def scrape_campaigns():

    mob_com_api_req = get("campaigns", {"include_opt_in_paths": 1})
    db, cur = _connect_db()

    # Capture Output into Beautiful Soup
    mob_com_campaign_soup = BeautifulSoup(mob_com_api_req.text, 'xml')

    # Assign Individual Campaigns to list
    mob_com_campaigns = mob_com_campaign_soup.find_all('campaign')

    # Regex Checker for Campaign Description with Format: Int OR Int,Int
    nid_run_id = re.compile('^(\d{1,6})(?:, ?(\d{1,6}))?')

    # Iterate through all Mobile Commons Campaigns and populate
    # "mobile_campaign_id_lookup" table. opt_in_path is the Primary Key to the
    # table.
    for campaign in mob_com_campaigns:
        print("****************************")
        name = campaign.find('name')
        description = campaign.find('description')
        campaign_id = campaign.get('id')
        opt_in_path = campaign.find_all('opt_in_path')
        for path in opt_in_path:
            path_name = path.find('name')
            matches = nid_run_id.match(description.text)
            if matches is not None:
                nid = matches.group(1)
                run_id = matches.group(2)
                if run_id is not None:
                    insert_campaign = "replace into users_and_activities.mobile_campaign_id_lookup VALUES ({0}, \"{1}\", {2}, \"{3}\", {4}, {5})".format(
                        path.get('id'), path_name.text.replace("\"", ""), campaign_id, name.text.replace("\"", ""), nid, run_id)
                    print(insert_campaign)
                    cur.execute(insert_campaign)
                    db.commit()
                else:
                    insert_campaign = "replace into users_and_activities.mobile_campaign_id_lookup VALUES ({0}, \"{1}\", {2}, \"{3}\", {4}, {5})".format(
                        path.get('id'), path_name.text.replace("\"", ""), campaign_id, name.text.replace("\"", ""), nid, 'NULL')
                    print(insert_campaign)
                    cur.execute(insert_campaign)
                    db.commit()
            else:
                insert_campaign = "replace into users_and_activities.mobile_campaign_id_lookup VALUES ({0}, \"{1}\", {2}, \"{3}\", {4}, {5})".format(
                    path.get('id'), path_name.text.replace("\"", ""), campaign_id, name.text.replace("\"", ""), 'NULL', 'NULL')
                print(insert_campaign)
                cur.execute(insert_campaign)
                db.commit()
        print("****************************")

    cur.close()
    db.close()

def convert_campaign_lookup_to_id():
    db, cur = _connect_db()
    cur.execute("SELECT * FROM users_and_activities.mobile_campaign_id_lookup")
    result = cur.fetchall()

    for row in result:
        if row['nid'] is not None:
            web_alpha = "0"
            if "alpha" in row['opt_in_path_id_name'] or "Alpha" in row['opt_in_path_id_name']:
                web_alpha = "1"

            nid = row['nid']
            campaign_id = row['mobile_campaign_id']
            opt_in_id = row['opt_in_path_id']
            web_alpha = "1"
            if row['run_nid'] is None:
                campaign_run = "NULL"
                insert_campaign = "insert ignore into users_and_activities.mobile_campaign_ids VALUES({0}, {1}, {2}, {3}, \"{4}\")".format(
                    nid, campaign_id, opt_in_id, web_alpha, campaign_run)
            else:
                campaign_run = row['run_nid']
                insert_campaign = "insert ignore into users_and_activities.mobile_campaign_ids VALUES({0}, {1}, {2}, {3}, {4})".format(
                    nid, campaign_id, opt_in_id, web_alpha, campaign_run)
            print(insert_campaign)
            cur.execute(insert_campaign)
            db.commit()

    cur.close()
    db.close()


def _connect_db():
    return database.connect({'conv':database.dec_to_float_converter()})
    