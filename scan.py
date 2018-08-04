import pymysql
import yaml
from rstformat import RstFormat


from pymysql.connections import Connection
from typing import Dict, List, Tuple
class Scan(object):

    def __init__(self, config: Dict[str, str]) -> None:
        self.config = config
        self.table_info = []
        self.info = {}

    def process(self) -> None:
            conn = pymysql.connect(host=self.config['host'],
                                   user=self.config['user'],
                                   password=self.config['password'],
                                   db=self.config['db'],
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

            self.scan_all(conn)
            conn.close()

    def scan_all(self, conn: Connection) -> None:
        sql = """    
            select
                table_name,
                table_comment
                from information_schema.TABLES
            where TABLE_SCHEMA = '%s'
        """ % (self.config['db'])

        with conn.cursor() as cursor:
            cursor.execute(sql)
            items = cursor.fetchall()

        for item in items:
            table = item['table_name']
            comment = item['table_comment']
            columns = self.scan_one(conn, table)
            self.table_info.append(
                {
                    'table_name': table,
                    'table_comment': comment,
                    'columns': columns
                }
            )

    def scan_one(self, conn: Connection, table_name: str) -> List[Tuple[str, str, str]]:
        sql = """
            show full fields from %s;
        """ % (table_name)

        with conn.cursor() as cursor:
            cursor.execute(sql)
            items = cursor.fetchall()

        return [(item['Field'], item['Comment'], item['Type']) for item in items]
