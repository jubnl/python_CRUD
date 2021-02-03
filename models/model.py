# made by https://github.com/jubnl

from .select_model import SelectModel
from .delete_model import DeleteModel
from .update_model import UpdateModel
from .insert_model import InsertModel


class Model(SelectModel,DeleteModel,UpdateModel,InsertModel):
    def __init__(self,table_name:str):
        super().__init__(table_name)


