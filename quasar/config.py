import os
from types import SimpleNamespace

env = os.environ.get("ENV")
default = {
    "CAMPAIGN_ACTIVITY_TABLE": "table",
    "ROGUE_PROGRESS_TABLE": "rogue",
    "DS_ROGUE_API_KEY": "dummy",
    "ROGUE_URI": "uri",
    "MYSQL_HOST": "localhost",
    "MYSQL_PORT": "3236",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "password",
    "MYSQL_DATABASE": "quasar",
    "host": "localhost", # phoenix_to_campaign_info_table
    "user": "root", # phoenix_to_campaign_info_table
    "pw": "password", # phoenix_to_campaign_info_table
    "mc_user": "user",
    "mc_pw": "password",
    "ns_client_id": "123",
    "ns_client_secret": "secret",
    "AMQP_URI": "amqp://user:password@localhost:5672/vhost?query",
    "AMQP_QUEUE": "queue",
    "AMQP_EXCHANGE": "exchage",
    "MYSQL_TABLE": "customerio"

}

config = SimpleNamespace(**default)

if env == "PROD" or env == "STAGING":
    import config as config
