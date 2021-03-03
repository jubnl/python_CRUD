# made by https://github.com/jubnl

import datetime

class Filter():


    def __init__(
        self, where:str=None, 
        order_by:dict=None,
        limit:int=None, 
        offset:int=None, 
        inner:dict=None, 
        right:dict=None, 
        left:dict=None
    ):
        self.where = where
        self.order_by = order_by
        self.limit = limit
        self.offset = offset
        self.inner = inner
        self.left = left
        self.right = right
    
    
        


    def __repr__(self):
        sql = ""
        
        if self.inner is not None:
            inner, on = self.inner.items()[0]
            sql+=f"INNER JOIN {inner} ON {on} "
            self.left = self.right = None
            
        if self.left is not None:
            inner, on = self.left.items()[0]
            sql+=f"LEFT JOIN {inner} ON {on}"
            self.inner = self.right = None
            
        if self.right is not None:
            inner, on = self.left.items()[0]
            sql+=f"RIGHT JOIN {inner} ON {on}"
            self.left = self.inner = None

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

