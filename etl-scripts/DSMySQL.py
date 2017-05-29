import MySQLdb

import config
from DSHelper import QuasarException

# MySQL Connector Library for Blade Platform.

class BladeMySQL:

    def __init__(self):
        """Setup MySQL Connector and credentials to Blade DB."""
        self.mysql_host = config.MYSQL_HOST
        self.mysql_port = config.MYSQL_PORT
        self.mysql_user = config.MYSQL_USER
        self.mysql_password = config.MYSQL_PASSWORD
        self.mysql_database = config.MYSQL_DATABASE
        # self.mysql_table = mysql_table

        self.mysql_connection = self.create_connection(mysql_host,
                                                        mysql_port,
                                                        mysql_user,
                                                        mysql_password,
                                                        mysql_database)
        self.mysql_cursor = self.mysql_connection.cursor()

    def create_connection(self, mysql_host, mysql_port, mysql_user,
                           mysql_password, mysql_database):
        try:
            conn = MySQLdb.connect(host=mysql_host,
                                   port=mysql_port,
                                   user=mysql_user,
                                   passwd=mysql_password,
                                   db=mysql_database,
                                   use_unicode=True,
                                   charset='utf8')
        except MySQLdb.InterfaceError as e:
            conn = False
            raise QuasarException(e)
        finally:
            return conn

    def create_disconnect(self):
        self.mysql_cursor.close()
        return self.mysql_connection()

    def mysql_query(self, query):
        """Parse and run DB query.

        Return On error, raise exception and log why.
        """
        try:
            self.mysql_cursor.execute(query)
            self.mysql_connection.commit()
            results = self.mysql_cursor.fetchall()
            return results
        except MySQLdb.DatabaseError as e:
            raise QuasarException(e)
