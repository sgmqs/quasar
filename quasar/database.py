import MySQLdb
import MySQLdb.converters
from .config import config


def dec_to_float_converter():
    converter = MySQLdb.converters.conversions.copy()
    converter[246] = float
    return converter


def connect(options={}):

    opts = {'user': config.user,
            'host': config.host,
            'port': config.port,
            'passwd': config.pw}

    opts.update(options)

    db = MySQLdb.connect(**opts)
    cur = db.cursor()

    if 'conv' in options:
        cur = db.cursor(MySQLdb.cursors.DictCursor)

    return db, cur
