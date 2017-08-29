import sys
import pandas as pd

from .config import config
from sqlalchemy import create_engine
from .database import Database as db
from pandas import DataFrame as df
from .utils import QuasarException
import datetime

class DataFrameDB:
    def __init__(self, options={}):

        # Defaults
        self.opts = {
            'user': config.MYSQL_USER,
            'host': config.MYSQL_HOST,
            'port': config.MYSQL_PORT,
            'passwd': config.MYSQL_PASSWORD,
            'db': config.MYSQL_DATABASE,
            'ssl': config.MYSQL_SSL,
            'use_unicode': True,
            'charset': 'utf8'
        }

        self.opts.update(options)

    def db_connect(self):
        # host = 'quasar-slave-new.c9ajz690mens.us-east-1.rds.amazonaws.com'
        # database = 'quasar'
        # login = open(path).read()
        # user_name = login.split(':')[0]
        # password = login.split(':')[1]

        engine = create_engine(
            'mysql+pymysql://' +
            self.opts['user'] +
            ':' +
            self.opts['passwd'] +
            '@' +
            self.opts['host'] +
            '/' +
            self.opts['database']
        )
        return engine

    def run_query(self, query):
        engine = self.db_connect()

        if '.sql' in query:
            q = open(query, 'r').read()
        else:
            q = query
        df = pd.read_sql_query(q, engine)
        return df

    def write_frame_to_db(self, frame, engine):
        df.to_sql(frame, engine)

class ETLMonitoring:
    def __init__(self):
        pass

    def teardown(self):
        db.disconnect()

    def construct_query_dict(description, query, query_set=None):
        if query_set==None:
            query_set = {}

        query_set[description] = query

        return query_set

    def get_status(query):
        try:
            value = DataFrameDB.run_query(query)
            out = int(value.iloc[0])
            return out
        except:
            out = str(QuasarException(sys.exc_info()[0]))
            return out

    def compile_statuses(queries):
        values = []
        descriptions = []
        ts = []
        table = []

        for query in queries.values():
            value = ETLMonitoring.get_status(query)
            values.append(value)
            time = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
            ts.append(time)
            thisTable = query.split('FROM')[1].split(' ')[1]
            table.append(thisTable)

        for description in queries.keys():
            descriptions.append(description)

        out = pd.DataFrame(
            {'query': descriptions,
             'output': values,
             'table': table,
             'timestamp': ts
             })
        return out


user_queries =  {
    'user_count':'SELECT count(*) FROM quasar.users',
    'user_user_count': 'SELECT count(distinct u.northstar_id) FROM quasar.users u',
    'ca_table_count': 'SELECT count(*) FROM quasar.campaign_activity c',
    'ca_post_count': 'SELECT count(distinct c.post_id) FROM quasar.campaign_activity c'
}
