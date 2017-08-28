import boto3
from bs4 import BeautifulSoup
from .config import config
from .database import Database
from .scraper import Scraper
from .utils import strip_str

scraper = Scraper('https://secure.mcommons.com', auth=(config.mc_user, config.mc_pw))
s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

def _get_profile(page):
    return scraper.getXml('/api/profiles', params={'page': page}) 

def _write_file(filename, data):
    s3.put_object(Key=filename, Bucket=config.MOCO_ARCHIVE_BUCKET,
                  Body=bytes(str(data), encoding='utf-8'))


def _get_start_page(db):
    querystr = ''.join(("SELECT last_page_scraped FROM ", config.MOCO_PROGRESS_TABLE))
    start_page = strip_str(db.query(querystr))
    return start_page

def _update_start_page(db, page):
    


def scrape_profiles(start_page=None):
    db = Database()
    if start_page is not None:
        page_num = start_page
    else:
        page_num = _get_start_page(db)
    while > 0:
        profiles = _get_profile(page_num).find_all('profile')
        if profiles is not None:
            for profile in profiles:
                filename = profile['id'] + '-' + profile.phone_number.string + '.xml'
                print(filename)
                _write_file(filename, profile)
            page_num += 1
        else:
            page_num = -1


def start_scrape():
    scrape_profiles()
