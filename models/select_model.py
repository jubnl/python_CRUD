# made by https://github.com/jubnl

from utilities.utilities import conn_db
import pymysql
from .return_object import QueryAllReturnObject, QueryOneReturnObject
import datetime

class SelectModel():


    def __init__(self, table_name:str):
        self.table_name = table_name


    def query_all_rows(self, distinct:bool=False, fields:list=None, filter:str=None, return_object:bool=False, return_sql_query:bool=False):
        """
        ### query_all_rows()
        #### parameters :
        - `distinct` (optional)     : Boolean, if True will remove duplicate, else will query duplicate rows too.

        - `fields` (optional)       : List of String (fields) to query.

        - `filter` (optional)       : Filter instance takes up to 4 arguments :
            - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
            - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
                - {'fieldName' : 'ASC', 'fieldName' : 'DESC'} etc..
            - `limit` (optional)        : Integer that limit how many rows we want to query.
            - `offset` (optional)       : Integer that will set an offset to the query. limit parameter is required to set an offset.

        - `return_object` (opional) : If set to True, will return an object. Each attribute correspond to a row. Attribute's name is `instance.result_n` n corresponding to the index of the row. 

        ##### Return
        The function returns either a list of dictionaries that contains the query's result or an object if `return_object` is set to True or a pymysql.Error or a pymysql.Warning.
        """


        # puts DISTINCT in query if set
        if distinct:
            sql = f"SELECT DISTINCT"
        else:
            sql = f"SELECT"
        
        # sets the fields to query
        if fields is not None:
            for field in fields:
                sql+=f" `{field}`,"
            sql = sql[:-1]
        else:
            sql+=" *"

        sql +=f" FROM `{self.table_name}` "

        if filter is not None:
            sql+=str(filter)
        conn = conn_db()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            datas = cur.fetchall()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            conn.rollback()
            conn.close()
            if return_sql_query is True:
                return sql, e
            return e
        if return_object:
            conn.close()
            if return_sql_query is True:
                return sql, QueryAllReturnObject(datas)
            return QueryAllReturnObject(datas)
        else:
            conn.close()
            if return_sql_query is True:
                return sql, datas
            return datas


    def query_one_row(self, filter:str, fields:list=None, return_object:bool=False, return_sql_query:bool=False):
        """
        ### query_one_row()
        #### parameters :
        - `filter` (required)       : Filter instance takes only one arguments :
            - `where` (required)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).

        - `fields` (optional)       : List of String (fields) to query.

        - `return_object` (opional) : If set to True, will return an object. Each attribute correspond to a field. Attribute's name is `instance.n` n corresponding to the field's name. 

        #### Return : 
        The function returns either a list of dictionaries that contains the query's result or an object if `return_object` is set to True or a pymysql.Error or a pymysql.Warning.
        """

        sql = "SELECT"

        if fields is not None:
            for field in fields:
                sql+=f" `{field}`,"
            sql = f"{sql[:-1]} FROM `{self.table_name}`"
        else:
            sql+=f" * FROM `{self.table_name}`"

        sql+=f" {str(filter)}"
        conn = conn_db()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            datas = cur.fetchone()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            conn.close()
            if return_sql_query is True:
                return sql, e
            return e
        else:
            if return_object:
                conn.close()
                if return_sql_query is True:
                    return sql, QueryOneReturnObject(datas)
                return QueryOneReturnObject(datas)
            else:
                conn.close()
                if return_sql_query is True:
                    return sql, datas
                return datas


    def count_rows(self, filter:str=None, return_object:bool=False, return_sql_query:bool=False):
        """
        ### count_rows()
        #### parameters :
        - `filter` (optional)       : Filter instance takes only one arguments :
            - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).

        - `return_object` (opional) : If set to True, will return an object. You can access the result by using the `count` attribute. 

        #### Return :
        Returns either an integer (how many rows are in the specified table) or an object if `return_object` is set to True or an Exception.
        """

        sql = f"SELECT COUNT(*) FROM `{self.table_name}`"

        if filter is not None:
            sql+=f" {str(filter)}"
        conn=conn_db()
        try:
            cur=conn.cursor()
            cur.execute(sql)
            count = cur.fetchone()
            cur.close()
        except (pymysql.Error, pymysql.Warning) as e:
            conn.rollback()
            conn.close()
            return e
        count['count'] = count['COUNT(*)']
        count.pop('COUNT(*)')
        if return_object:
            conn.close()
            if return_sql_query is True:
                return sql, QueryOneReturnObject(count)
            return QueryOneReturnObject(count)
        else:
            conn.close()
            if return_sql_query is True:
                return sql, int(count['count'])
            return int(count['count'])


