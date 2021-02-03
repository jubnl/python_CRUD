# made by https://github.com/jubnl

import datetime

class Filter():


    def __init__(self, where:str=None, order_by:dict=None, limit:int=None, offset:int=None):
        self.where = where
        self.order_by = order_by
        self.limit = limit
        self.offset = offset


    def __repr__(self):
        sql = ""

        if self.where is not None:
            sql+=f"WHERE {self.where} "

        if self.order_by is not None:
            keys = list(self.order_by.keys())
            values = list(self.order_by.values())
            sql+=f"ORDER BY `{keys[0]}` {values[0]}"
            if len(self.order_by) > 1:
                for i in range (1,len(self.order_by)):
                    sql+=f", `{keys[i]}` {values[i]}"
            sql+=" "

        if self.limit is not None:
            if self.offset is None:
                self.offset = 0
            sql+=f"LIMIT {self.limit} OFFSET {self.offset}"

        return sql

