# Python file to define class object for MySQL interaction
import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import mysql.connector as mysql
from config import DB_SETTINGS


class MySQLDBConn:
    db_config = DB_SETTINGS
    conn = mysql.connect(pool_name = "mypool",
                              pool_size = 4,
                              charset="utf8mb4",
                              **DB_SETTINGS)
    @classmethod
    def execute_query(cls, sql_query = "select * from page limit 5;"):
        cursor = None
        try:
            with cls.conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                cursor.close()
                return result
        except mysql.Error as e:
            print("Error while running query on  MySQL: ", e)
            raise e
        except Exception as e:
            print("generic exception", e)
            raise e
        finally:
            # closing database connection.
            if cursor:
                cursor.close()

    @classmethod
    def execute_sql_file(cls, sql_file_path):
        cursor = None
        try:
            with cls.conn.cursor(dictionary=True) as cursor:
                with open(sql_file_path, mode='r', encoding='utf-8-sig') as f:
                    cursor.execute(f.read())
                cursor.close()
                return result
        except mysql.Error as e:
            print("Error while connecting to MySQL: ", e)
            return False
        finally:
            # closing database connection.
            if cursor:
                cursor.close()

    @classmethod
    def execute_sql_cmd(cls, sql_command):
        """
        Executes command line sql queries on shell.
        """
        try:
            command = sql_command.split()
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            p.communicate()
            return True
        except Exception as e:
            print("Exception occured while executing command line sql query: {}, exception: {}".format(sql_command, str(e)))
            return False




if __name__ == '__main__':
    print(MySQLDBConn.execute_query())
