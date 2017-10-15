import boto3
from .config import config
from .database import Database
from .scraper import Scraper
from .utils import strip_str

scraper = Scraper('https://secure.mcommons.com',
                  auth=(config.mc_user, config.mc_pw))
s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

db = Database()


def _get_profile(page):
    return scraper.getXml('/api/profiles', params={'page': page})


def _update_campaigns(db):
    # First run of this depends on manually setting if scrape is completed
    # or not in Quasar DB.
    campaigns = scraper.getXml('/api/campaigns').find_all('campaign')
    for campaign in campaigns:
        querystr = ''.join(("INSERT INTO ", config.MOCO_CAMPAIGN_LIST_TABLE,
                            "(campaign_id) VALUES ({}) ",
                            "ON DUPLICATE KEY UPDATE ",
                            "campaign_id = {}",
                            "")).format(campaign['id'], campaign['id'])
        db.query(querystr)


def _get_campaigns(db):
    querystr = ''.join(("SELECT * FROM ", config.MOCO_CAMPAIGN_LIST_TABLE))
    return db.query(querystr)


def _get_campaign(db):
    querystr = ''.join(("SELECT * FROM ", config.MOCO_CAMPAIGN_LIST_TABLE,
                        " WHERE status = 'unlocked' AND ",
                        "campaign_scrape_completed <> TRUE ",
                        "ORDER BY campaign_id DESC LIMIT 1"))
    return db.query(querystr)


def _set_campaign_page(db, page, campaign):
    querystr = ''.join(("UPDATE ", config.MOCO_CAMPAIGN_LIST_TABLE,
                        " SET last_page = {} WHERE campaign_id = {}",
                        "")).format(page, campaign)
    db.query(querystr)


def _set_status(db, status, campaign):
    querystr = ''.join(("UPDATE ", config.MOCO_CAMPAIGN_LIST_TABLE,
                        " SET status = '{}' WHERE campaign_id = {}",
                        "")).format(status, campaign)
    db.query(querystr)


def _set_campaign_completed(db, campaign):
    querystr = ''.join(("UPDATE ", config.MOCO_CAMPAIGN_LIST_TABLE,
                        " SET campaign_scrape_completed = TRUE, ",
                        " status = '{}' WHERE campaign_id = {}",
                        "")).format("done", campaign)
    db.query(querystr)


def _get_message(campaign, page):
    return scraper.getXml('/api/messages', params={'include_profile': 'true',
                          'campaign_id': campaign, 'page': page})


def _write_file(filename, data):
    s3.put_object(Key=filename, Bucket=config.MOCO_ARCHIVE_BUCKET,
                  Body=bytes(str(data), encoding='utf-8'))


def _get_profile_start_page(db):
    querystr = ''.join(("SELECT last_page_scraped FROM ",
                        config.MOCO_PROGRESS_TABLE))
    start_page = strip_str(db.query(querystr))
    return start_page


def _update_profile_start_page(db, page):
    querystr = ''.join(("UPDATE ", config.MOCO_PROGRESS_TABLE,
                        " SET last_page_scraped = {}")).format(page)
    db.query(querystr)


def scrape_messages():
    _update_campaigns(db)
    campaign = _get_campaign(db)
    try:
        while campaign is not None:
            page = campaign[0][1]
            _set_status(db, "locked", campaign[0][0])
            messages = _get_message(campaign[0][0],
                                    page).find_all('message')
            while messages != []:
                for message in messages:
                    filename = (str(campaign[0][0]) + '-' +
                                message['id'] + '-' +
                                'message' + '.xml')
                    _write_file(filename, message)
                    print("Wrote message {} for campaign {}, "
                          "page {}".format(filename,
                                           campaign[0][0], page))
                page += 1
                _set_campaign_page(db, page, campaign[0][0])
                messages = _get_message(campaign[0][0],
                                        page).find_all('message')
            _set_campaign_completed(db, campaign[0][0])
            campaign = _get_campaign(db)
    except KeyboardInterrupt:
        _set_status(db, "unlocked", campaign[0][0])


def scrape_profiles(start_page=None):
    if start_page is not None:
        page_num = str(start_page)
    else:
        page_num = _get_profile_start_page(db)
    profiles = _get_profile(page_num).find_all('profile')
    while profiles != []:
        profile_num = 1
        for profile in profiles:
            filename = (profile['id'] + '-' +
                        profile.phone_number.string + '.xml')
            _write_file(filename, profile)
            print("Wrote profile {}/1000 of page "
                  "{}".format(profile_num, page_num))
            profile_num += 1
        interim_cast = int(page_num)
        interim_cast += 1
        page_num = str(interim_cast)
        print(page_num)
        _update_profile_start_page(db, str(page_num))
        profiles = _get_profile(page_num).find_all('profile')


def start_profile_scrape():
    scrape_profiles()


def start_message_scrape():
    scrape_messages()
