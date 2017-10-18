import json, os

import boto3, xmltodict
from .config import config
from .database import Database
from .utils import strip_str

s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

db = Database()

def _insert_profile(db, profile):
    str = ''.join(("REPLACE INTO quasar.moco_profile_import ",
                   "VALUES ({}, '{}', '{}', '{}', '{}', '{}', ",
                   "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', ",
                   "'{}', POINT({}, {}))",
                   "")).format(
                            profile['@id'], 
                            strip_str(profile['phone_number']),
                            profile['created_at'], profile['updated_at'],
                            strip_str(profile['status']), 
                            strip_str(profile['opted_out_at']),
                            strip_str(profile['opted_out_source']),
                            strip_str(profile['address']['street1']),
                            strip_str(profile['address']['street2']),
                            strip_str(profile['address']['city']),
                            strip_str(profile['address']['state']),
                            profile['address']['postal_code'],
                            strip_str(profile['address']['country']),
                            strip_str(profile['location']['city']),
                            strip_str(profile['location']['state']),
                            profile['location']['postal_code'],
                            strip_str(profile['location']['country']),
                            profile['location']['latitude'],
                            profile['location']['longitude'])
    db.query(str)

def import_profiles():
    for file in os.listdir(config.MOCO_PROFILE_DIR):
        moco_xml = open(''.join((config.MOCO_PROFILE_DIR, "/{}",
                                 "")).format(file), "r").read()
        profile = xmltodict.parse(moco_xml)['profile']
        _insert_profile(db, profile)

def convert_to_json_file():
    pass

def import_filenames():
    pass
    
def main_import_profiles():
    import_profiles()
