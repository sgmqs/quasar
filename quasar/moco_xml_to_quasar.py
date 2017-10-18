import json, os

import boto3, xmltodict
from .config import config
from .database import Database

s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

db = Database()

def update_filenames():
    pass


def _get_filename_batch(marker=''):
    s3.list_objects(Bucket=config.MOCO_ARCHIVE_BUCKET)

def _insert_profile(db, profile):
    str = ''.join(("REPLACE INTO quasar.moco_profile_import ",
                   "(moco_id, mobile, created_at, updated_at, ",
                   "status, opted_out_at, opted_out_source, ",
                   "addr_street1, addr_street2, addr_city, ",
                   "addr_state, addr_zip, addr_country, ",
                   "loc_city, loc_state, loc_zip, loc_country, ",
                   "loc_latlong) VALUES({}, {}, {}, {}, {}, {}, {}, ",
                   "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, POINT({}, {}))",
                   "")).format(
                            profile['@id'], profile['phone_number'],
                            profile['created_at'], profile['updated_at'],
                            profile['status'], profile['opted_out_at'],
                            profile['opted_out_source'],
                            profile['address']['street1'],
                            profile['address']['street2'],
                            profile['address']['city'],
                            profile['address']['state'],
                            profile['address']['postal_code'],
                            profile['address']['country'],
                            profile['location']['city'],
                            profile['location']['state'],
                            profile['location']['postal_code'],
                            profile['location']['country'],
                            profile['location']['latitude'],
                            profile['location']['longitude'])
    print(str)

def import_profiles:
    for file in os.listdir(config.MOCO_PROFILE_DIR):
        moco_xml = open(file, "r").read()
        profile = xmltodict.parse(moco_object)['profile']
        _insert_profile(db, profile)


# import xmltodict, json
# moco_xml = open("filename", "r").read()
# moco_json = xmltodict.parse(moco_object)
# profile = xmltodict.parse(moco_object)['profile']
# print(json.dumps(moco_jsonified, indent=4, sort_keys=True)
# 
# 
# moco_id INT, - moco_json['profile']['@id']
# mobile VARCHAR(24), - moco_json['profile']['phone_number']
# created_at DATETIME, - moco_json['profile']['created_at']
# updated_at DATETIME, - moco_json['profile']['updated_at']
# status VARCHAR(24), - moco_json['profile']['status']
# opted_out_at DATETIME, - moco_json['profile']['opted_out_at']
# opted_out_source VARCHAR(48), - moco_json['profile']['opted_out_source']
# addr_street1 VARCHAR(24), - moco_json['profile']['address']['street1']
# addr_street2 VARCHAR(24), - moco_json['profile']['address']['street2']
# addr_city VARCHAR(24), - moco_json['profile']['address']['city']
# addr_state VARCHAR(4), - moco_json['profile']['address']['state']
# addr_zip INT, - moco_json['profile']['address']['postal_code']
# addr_country VARCHAR(4), - moco_json['profile']['address']['country']
# loc_city VARCHAR(24), - moco_json['profile']['location']['city']
# loc_state VARCHAR(4), - moco_json['profile']['location']['state']
# loc_zip INT, - moco_json['profile']['location']['postal_code']
# loc_country VARCHAR(4), - moco_json['profile']['location']['country']
# loc_latlong POINT, - moco_json['profile']['location']['latitude'], moco_json['profile']['location']['longitude']
