# made by https://github.com/jubnl

from utilities.utilities import conn_db
import pymysql
import datetime


class DeleteModel():


    def __init__(self, table_name:str):
        self.table_name = table_name


    def delete_row(self, filter:str=None):
        """
        ### delete_row(filter=None)
        #### Parameters :
        - `filter` (optional)       : Filter instance, takes up to 3 arguments :
            - `where` (optional)    : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
            - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
                - {'fieldName' : 'ASC', 'fieldName' : 'DESC'}
            - `limit` (optional)        : Integer that limit how many rows we want to delete.

        ##### Return
        The function returns either True if the delete went well or a pymysql.Error or a pymysql.Warning.
        """

        sql = f"DELETE FROM `{self.table_name}` "

        if filter is not None:
            sql+=str(filter)

        try:
            conn = conn_db()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            return e
        else:
            return True


