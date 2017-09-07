import sys
import pandas as pd

from .config import config
from sqlalchemy import create_engine
from .database import Database as db
from .utils import QuasarException
import datetime

class DataFrameDB:
    def __init__(self, options={}):

        # Defaults
        self.opts = {
            'user': config.MYSQL_USER,
            'host': config.MYSQL_HOST,
            'passwd': config.MYSQL_PASSWORD,
            'db': config.MYSQL_DATABASE,
            'use_unicode': True,
            'charset': 'utf8'
        }

        self.opts.update(options)

    def db_connect(self):

        self.engine = create_engine(
            'mysql+pymysql://' +
            self.opts['user'] +
            ':' +
            self.opts['passwd'] +
            '@' +
            self.opts['host'] +
            '/' +
            self.opts['database']
        )
        return self.engine

    def run_query(self, query):
        self.engine = self.db_connect()

        if '.sql' in query:
            q = open(query, 'r').read()
        else:
            q = query
        self.df = pd.read_sql_query(q, self.engine)
        return self.df


class ETLMonitoring:
    def __init__(self):
        self.etl_queries = {
            'user_count': 'SELECT count(*) FROM quasar.users',
            'user_user_count': 'SELECT count(distinct u.northstar_id) FROM quasar.users u',
            'ca_table_count': 'SELECT count(*) FROM quasar.campaign_activity c',
            'ca_post_count': 'SELECT count(distinct c.post_id) FROM quasar.campaign_activity c'
        }

    @staticmethod
    def teardown(self):
        db.disconnect(self)

    @staticmethod
    def construct_query_dict(self, description, query, query_set=None):
        if query_set==None:
            query_set = {}

        query_set[description] = query

        return query_set

    def get_value(self, query):
        try:
            value = DataFrameDB.run_query(query)
            out = int(value.iloc[0])
            return out
        except:
            out = str(QuasarException(sys.exc_info()[0]))
            return out

    def compile_statuses(self, queries):
        values = []
        descriptions = []
        ts = []
        table = []

        for query in queries.values():
            value = self.get_value(query)
            values.append(value)
            time = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
            ts.append(time)
            this_table = query.split('FROM')[1].split(' ')[1]
            table.append(this_table)

        for description in queries.keys():
            descriptions.append(description)

        out = pd.DataFrame(
            {'query': descriptions,
             'output': values,
             'table': table,
             'timestamp': ts
             })
        return out

    @staticmethod
    def write_to_monitoring_table(table):
        table.to_sql(
            name='monitoring',
            con=DataFrameDB.db_connect(DataFrameDB.opts),
            schema='quasar',
            if_exists='append'
        )

    def extract_latest_value(self, table, desc):
        max_query = \
            "SELECT  \
                m.output  \
            FROM quasar.monitoring m  \
            INNER JOIN ( \
            SELECT \
                t.table, \
                t.query,  \
                max(t.timestamp) AS max_created \
            FROM quasar.monitoring t \
            GROUP BY t.table, t.query \
                ) m ON m.max_created = u.timestamp \
            WHERE m.table = '" + table + "'  \
            AND m.query = '" + desc + "'"
        value = self.get_value(max_query)
        return value

    def extract_second_latest_value(self, table, desc):
        max_2_query = \
            "SELECT \
                m.output \
            FROM quasar.monitoring m \
            INNER JOIN \
                (SELECT \
                    max(t.timestamp) AS ts_2 \
                FROM quasar.monitoring t \
                WHERE t.table = '" + table + "' \
                AND t.query = '" + desc + "' \
                AND \
                t.timestamp < (SELECT max(t1.timestamp)  \
                                FROM quasar.monitoring t1 \
                                WHERE t1.table = '" + table + "' AND t1.query = '" + desc + "') \
                ) ts2 ON ts2.ts_2 = u.timestamp \
            WHERE t1.table = '" + table + "' AND t1.query = '" + desc + "'"
        value = self.get_value(max_2_query)
        return value

    def compare_latest_values(self, table, desc):
        latest_value = self.extract_latest_value(table, desc)
        second_latest_value = self.extract_second_latest_value(table, desc)

        if latest_value > second_latest_value:
            message = 'Passed'
        else:
            message = 'Issue Detected'
        report = table + ' ' + desc + ' ' + message

        return report

    def monitor(self, queries):
        messages = []
        frame = self.compile_statuses(self.etl_queries)
        self.write_to_monitoring_table(frame)

        for table in queries:
            this_table = table.split('FROM')[1].split(' ')[1]
            this_desc = table.keys()
            this_message = self.compare_latest_values(this_table, this_desc)
            messages.append(this_message)

        return messages
