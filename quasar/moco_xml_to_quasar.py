import json

import boto3, xmltodict
from .config import config
from .database import Database

s3 = boto3.client(
    's3',
    aws_access_key_id=config.QUASAR_AWS_S3_ID,
    aws_secret_access_key=config.QUASAR_AWS_S3_SECRET)

db = Database()

def _update_profile_filename()
