# made by https://github.com/jubnl

from utilities.utilities import conn_db
import pymysql
import datetime


class InsertModel():


    def __init__(self, table_name:str):
        self.table_name = table_name


    def insert_into_single_record(self, fields_values:dict, return_sql_query:bool=False):
        """
        ### insert_into_single_record()
        #### parameters :

        - `fields_values` (optional): Dictionary that contains the values that you want to insert. The dictionary needs to follow this template :.
                {'fieldName' : 'value', 'fieldName' : 'value'}
        etc..

        ##### Return
        The function returns either True if the insert went well or a pymysql.Error or a pymysql.Warning.
        """


        sql = f"INSERT INTO {self.table_name} ("

        fields = list(fields_values.keys())
        values = list(fields_values.values())

        for field in fields:
            sql+=f"`{field}`, "

        sql = sql[:-2]+") VALUES ("

        for value in values:
            if isinstance(value,str):
                sql+=f"'{value}', "
            else:
                sql+=f"{value}, "

        sql = sql[:-2]+")"
        conn=conn_db()
        try:
            cur=conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            conn.rollback()
            conn.close()
            if return_sql_query is True:
                return sql, e
            return e
        conn.close()
        if return_sql_query is True:
                return sql, True
        return True


