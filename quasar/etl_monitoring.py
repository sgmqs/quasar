import sys
import os
import datetime as dt
import pandas as pd


from .config import config
from .utils import QuasarException
from sqlalchemy import create_engine
from slackclient import SlackClient


class DataFrameDB:
    def __init__(self, opts={}):

        self.opts = {
            'user': config.MYSQL_USER,
            'host': config.MYSQL_HOST,
            'password': config.MYSQL_PASSWORD,
            'db': config.MYSQL_DATABASE,
            'port': config.MYSQL_PORT,
            'use_unicode': True,
            'charset': 'utf8'
        }

        self.engine = create_engine(
            'mysql+mysqldb://' +
            self.opts['user'] +
            ':' +
            self.opts['password'] +
            '@' +
            self.opts['host'] +
            ':' +
            self.opts['port'] +
            '/' +
            self.opts['db'])

    def run_query(self, query):
        if '.sql' in query:
            q = open(query, 'r').read()
        else:
            q = query
        df = pd.read_sql_query(q, self.engine)
        return df


class ETLMonitoring:
    def __init__(self):
        db_opts = {}
        self.db = DataFrameDB(db_opts)

        self.etl_queries = {
            'user_count':
                'SELECT count(*) FROM quasar.users',
            'user_distinct_user_count':
                'SELECT count(distinct u.northstar_id) '
                'FROM quasar.users u',
            'ca_table_count':
                'SELECT count(*) FROM quasar.campaign_activity c',
            'ca_post_count':
                'SELECT count(distinct c.post_id) '
                'FROM quasar.campaign_activity c'
        }

    @staticmethod
    def teardown(self):
        self.db.disconnect(self)

    @staticmethod
    def construct_query_dict(description, query, query_set=None):
        if query_set is None:
            query_set = {}

        query_set[description] = query

        return query_set

    def get_value(self, query):
        try:
            value = self.db.run_query(query)
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
            time = dt.datetime.now().strftime("%m-%d-%y %H:%M:%S")
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
            WHERE t.table = '" + table + "' AND t.query = '" + desc + "' \
                ) tim ON tim.max_created = m.timestamp \
            WHERE m.table = '" + table + "'  \
            AND m.query = '" + desc + "';"
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
                                WHERE t1.table = '" + table + "'  \
                                AND t1.query = '" + desc + "') \
                ) ts2 ON ts2.ts_2 = m.timestamp \
            WHERE m.table = '" + table + "' AND m.query = '" + desc + "';"
        value = self.get_value(max_2_query)
        return value

    def compare_latest_values(self, table, desc):
        latest_value = self.extract_latest_value(table, desc)
        second_latest_value = self.extract_second_latest_value(table, desc)

        try:
            if latest_value > second_latest_value:
                message = "Passed - Latest Count = " + \
                          str(latest_value) + \
                          " Previous Value = " + \
                          str(second_latest_value) +  \
                          ", Count increased by " + \
                          str(latest_value - second_latest_value)
            elif latest_value == second_latest_value:
                message = "Failed - Count Unchanged," \
                          " Latest Count = " + \
                          str(latest_value) + \
                          " Previous Value = " + \
                          str(second_latest_value)
            elif latest_value < second_latest_value:
                message = "Failed - Count Decreased," \
                          " Latest Count = " + \
                          str(latest_value) + \
                          " Previous Value = " + \
                          str(second_latest_value)
            else:
                message = 'Failed - Unspecified Error'
        except:
            message = str(QuasarException(sys.exc_info()[0]))
        report = table + " " + desc + " " + message

        return report

    def write_to_monitoring_table(self, table):
        table.to_sql(
            name='monitoring',
            con=self.db.engine,
            schema='quasar',
            if_exists='append'
        )

    def monitor(self):
        messages = []
        frame = self.compile_statuses(self.etl_queries)
        self.write_to_monitoring_table(frame)

        for index, row in frame.iterrows():
            this_table = row['table']
            this_desc = row['query']
            this_message = self.compare_latest_values(this_table, this_desc)
            messages.append(this_message)
        return messages


def run_monitoring():
    mon = ETLMonitoring()
    out = mon.monitor()

    client_token = os.environ.get('ETLMON_SLACKBOT_TOKEN')
    sc = SlackClient(client_token)
    sc.api_call(
        "chat.postMessage",
        channel="#quasar-notifications",
        text=out
    )
