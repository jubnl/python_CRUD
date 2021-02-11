# made by https://github.com/jubnl

from utilities.utilities import conn_db
import pymysql
import datetime


class UpdateModel():


    def __init__(self,table_name:str):
        self.table_name = table_name


    def update_rows(self, fields_values:dict, filter:str=None, return_sql_query:bool=False):
        """
        ### update_rows()
        #### parameters :
        - `fields_values` (optional): Dictionary that contains colomns' name and their new values. The dictionary needs to follow this template :
                {'fieldName' : 'value', 'fieldName' : 'value'}
        etc..

        - `filter` (optional)       : Filter instance takes only one arguments :
            - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
            - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
                - {'fieldName' : 'ASC', 'fieldName' : 'DESC'} etc..
            - `limit` (optional)        : Integer that limit how many rows we want to update.

        ##### Return
        The function returns either True if the update went well or a pymysql.Error or a pymysql.Warning.
        """

        sql = f"UPDATE `{self.table_name}` SET"

        for field in fields_values:
            value = fields_values[field]
            if isinstance(value, str):
                sql+=f" `{field}` = '{value}',"
            else:
                sql+=f" `{field}` = {value},"
        
        sql = sql[:-1]

        if filter is not None:
            sql+=f" {str(filter)}"
        conn = conn_db()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            conn.rollback()
            conn.close()
            if return_sql_query is True:
                return sql, e
            return e
        else:
            conn.close()
            if return_sql_query is True:
                return sql, True
            return True


