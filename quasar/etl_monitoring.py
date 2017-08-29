import sys
import pandas as pd
from .config import config
from .database import Database
from pandas import DataFrame as df
from .utils import QuasarException

class dataframe_db:
    def __init__(self):
        pass

    def db_connect(path):
        host = 'quasar-slave-new.c9ajz690mens.us-east-1.rds.amazonaws.com'
        database = 'quasar'
        login = open(path).read()
        user_name = login.split(':')[0]
        password = login.split(':')[1]

        engine = create_engine('mysql+pymysql://' + user_name + ':' + password + '@' + host + '/' + database)
        return engine


    def run_query(query, credentials):
        import pandas as pd
        engine = db_connect(credentials)

        if '.sql' in query:
            q = open(query, 'r').read()
        else:
            q = query
        df = pd.read_sql_query(q, engine)
        return df

    def write_frame_to_db(self, frame):
        df.to_sql(frame, engine)

class ETLMonitoring:
    def __init__(self):
        pass

    def teardown(self):
        self.db.disconnect()

    def construct_query_dict(description, query, query_set=None):
        if query_set==None:
            query_set = {}

        query_set[description] = query

        return query_set

    def get_status(query):
        try:
            value = dataframe_db.run_query(query, credentials)
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
            value = get_status(query)
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
