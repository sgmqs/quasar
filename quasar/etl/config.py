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
    "MYSQL_DATABASE": "quasar"
}

config = SimpleNamespace(**default)

if env == "PROD" or env == "STAGING":
    import config as config
