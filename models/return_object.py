# made by https://github.com/jubnl
import datetime


class QueryAllReturnObject():


    def __init__(self,datas:list):
        for data in datas:
            exec(f"self.result_{datas.index(data)} = {data}")


class QueryOneReturnObject():


    def __init__(self, datas:dict):
        keys = list(datas.keys())
        values = list(datas.values())
        for key in keys:
            if isinstance(values[keys.index(key)],str):
                exec(f"self.{key} = '{values[keys.index(key)]}'")
            else:
                exec(f"self.{key} = {values[keys.index(key)]}")


