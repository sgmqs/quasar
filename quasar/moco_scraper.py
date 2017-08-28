import boto3
from bs4 import BeautifulSoup
from .config import config
from .database import Database
from .scraper import Scraper

scraper = Scraper('https://secure.mcommons.com', auth=(config.mc_user, config.mc_pw))
# connector = boto.connect_s3(config.QUASAR_AWS_S3_ID, config.QUASAR_AWS_S3_SECRET)
# bucket = connector.get_bucket(config.MOCO_ARCHIVE_BUCKET)
# s3 = boto.s3.key.Key(bucket)

s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

def _get_profile(page):
    return scraper.getXml('/api/profiles', params={'page': page}) 

def _write_file(filename, data):
    s3.put_object(Key=filename, Bucket=config.MOCO_ARCHIVE_BUCKET,
                  Body=bytes(str(data), encoding='utf-8'))

def scrape_profiles(start_page):
    page_num = start_page
    while page_num <= 2:
        profiles = _get_profile(page_num).find_all('profile')
        for profile in profiles:
            filename = profile['id'] + '-' + profile.phone_number.string + '.xml'
            print(filename)
            _write_file(filename, profile)
        page_num += 1


def start_scrape():
    scrape_profiles(1)
