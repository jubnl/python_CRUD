# CRUD with PyMySQL

## Getting started

Start by cloning this repository somewhere and copy all the folders / files at the root of your web project.
Your project should look like this :
```
root_of_your_project
│
├───config
│   └───db_config.json
├───models
│   ├───delete_model.py
│   ├───filter.py
│   ├───insert_model.py
│   ├───model.py
│   ├───return_object.py
│   ├───select_model.py
│   └───update_model.py
├───utilities
│   └───utilities.py
├───README.md
├───requirements.txt
│   
└───your_main.py
```

### External libraries
All libraries are in requirements.txt . Just open a terminal or a command prompt in root_of_your_project and type : `pip install -r requirements.txt`

### Configuration
To connect the CRUD to a database you have to edit [config/db_config.json](config/db_config.json) .

`db_host` : String, either an IP address or a FQDN.

`db_port` : Integer, that's the database's port

`db_user` : String, your username

`db_password` : String, your password

`db_name` : String, The database's name

### Using the Model

Then you can import the Model and Filter in your_main.py and use it.
```python
from models.model import Model
from models.filter import Filter
import pymysql.Error, pymysql.Warning

model = Model("table_name")
filter = Filter(where="`field_name` > 10")

query = model.query_all_rows(filter=filter)

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  for row in query:
    print(row)

query = model.query_all_rows(return_object=True)

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  for i in list(query.__dict__.keys()):
    exec(f"print(query.{i})")
```

## Model class
This class takes one argument required : the table's name.
```python
from models.model import Model

model = Model("table_name")

query = model.query_all_rows()

print(query)
```

## Filter class
This class takes up to 4 arguments :
- `where` : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)). More informations [here](#about-where-parameter).
- `order_by` : Dictionary that contains sorting values. The dictionary needs to follow this template :
  - `{'fieldName' : 'ASC', 'fieldName' : 'DESC'}` etc..
- `limit` : Integer that limit how many rows we want to query.
- `offset` : Integer that will set an offset to the query. limit parameter is required to set an offset.

Here is an exemple :
```python
from models.filter import Filter
from models.model import Model

model = Model("table_name")

filter = Filter(where="`id` > 3", order_by={'field_name_1':'ASC', 'field_name_2':'DESC'}, limit=5, offset=12)

query = model.query_all_rows(filter=filter)

print(query)
```


## About `where` parameter
The `where` parameter is a String that contains all your conditions.

Fields absolutly need to be surrounded by `` so for exemple here is a where clause:
```python
where = "`field` = 'value'"
```
You can find all arguments you can pass [here](https://www.techonthenet.com/mariadb/where.php).

Just remeber that all fields in the where clause needs to be surrounded by ``.

## Create

There is for the moment only one method that can insert one row at the time :
### ```insert_into_single_record(field_name=None)```

#### parameters :
- `fields_values` (optional): Dictionary that contains the values that you want to insert. The dictionary needs to follow this template :.
  - `{'fieldName' : 'value', 'fieldName' : 'value'}`etc..

##### Return
The function returns either True if the insert went well or a pymysql.Error or a pymysql.Warning.


#### Usage :
```python
from models.model import Model
import pymysql.Error, pymysql.Warning

model = Model("table_name")
query = model.insert_into_single_record(field_name={'field_name':'value', 'field_name':'value'})

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  print("Row inserted !") # query = True if no errors
```


## Read
There are 3 different methods :
- [`query_all_rows`](#query_all_rowsdistinctfalse-fieldsnone-filternone-return_objectfalse)
- [`query_one_row`](#query_one_rowfilter-fieldsnone-return_objectfalse)
- [`count_rows`](#count_rowsfilternone-return_objectfalse)

### ```query_all_rows(distinct=False, fields=None, filter=None, return_object=False)```
#### parameters :
- `distinct` (optional)     : Boolean, if True will remove duplicate, else will query duplicate rows too.

- `fields` (optional)       : List of String (fields) to query.

- `filter` (optional)       : Filter instance takes up to 4 arguments :
    - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
    - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
      - {'fieldName' : 'ASC', 'fieldName' : 'DESC'} etc..
    - `limit` (optional)        : Integer that limit how many rows we want to query.
    - `offset` (optional)       : Integer that will set an offset to the query. limit parameter is required to set an offset.

- `return_object` (opional) : If set to True, will return an object. Each attribute correspond to a row. Attribute's name is `instance.row_n` n corresponding to the index (starting from 0) of the row. 

##### Return
The function returns either a list of dictionaries that contains the query's result or an object if `return_object` is set to True or a pymysql.Error or a pymysql.Warning.

#### Usage :
```python
from models.model import Model
from models.filter import Filter
import pymysql.Error, pymysql.Warning

model = Model("table_name")

filter = Filter(where="`field_name` > 100")

query = model.query_all_rows(distinct=True, fields=['field_1', 'field_2'], filter=filter)

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  for row in query:
    print(row)
```

### ```query_one_row(filter, fields=None, return_object=False)```
#### parameters :
- `filter` (required)       : Filter instance takes only one arguments :
    - `where` (required)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).

- `fields` (optional)       : List of String (fields) to query.

- `return_object` (opional) : If set to True, will return an object. Each attribute correspond to a field. Attribute's name is `instance.n` n corresponding to the field's name. 

#### Return : 
The function returns either a list of dictionaries that contains the query's result or an object if `return_object` is set to True or a pymysql.Error or a pymysql.Warning.

#### Usage :
```python
from models.model import Model
from models.filter import Filter
import pymysql.Error, pymysql.Warning

model = Model("table_name")
filter = Filter(where="`field_name` = 1")

query = model.query_one_row(filter=filter)

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  print(query)
```

### ```count_rows(filter=None, return_object=False)```
#### parameters :
- `filter` (optional)       : Filter instance takes only one arguments :
    - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).

- `return_object` (opional) : If set to True, will return an object. You can access the result by using the `count` attribute. 

#### Return :
Returns either an integer (how many rows are in the specified table) or an object if `return_object` is set to True or an Exception.

#### Usage :
```python
from models.model import Model
import pymysql.Error, pymysql.Warning

model = Model("table_name")

query = model.count_rows()

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  print(query)
```
## Update
### ```update_rows(fields_value=None, filter=None)```
#### Parameters :
- `fields_values` (optional): Dictionary that contains colomns' name and their new values. The dictionary needs to follow this template :
  - {'fieldName' : 'value', 'fieldName' : 'value'} etc..

- `filter` (optional)       : Filter instance takes only one arguments :
    - `where` (optional)        : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
    - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
        - {'fieldName' : 'ASC', 'fieldName' : 'DESC'} etc..
    - `limit` (optional)        : Integer that limit how many rows we want to update.

##### Return
The function returns either True if the update went well or a pymysql.Error or a pymysql.Warning.

#### Usage :
```python
from models.model import Model
from models.filter import Filter
import pymysql.Error, pymysql.Warning

model = Model("table_name")
filter = Filter(where="`field_name` = 1")

query = model.update_rows(fields_value={'field_1':'value', 'field_2':'value'}, filter=filter")

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  print("Update successful") # query = True if no errors
```

## Delete
### ```delete_row(filter=None)```
#### Parameters :
- `filter` (optional)       : Filter instance, takes up to 3 arguments :
    - `where` (optional)    : String that contains a WHERE SQL clause (without 'WHERE', just the condition(s)).
    - `order_by` (optional)     : Dictionary that contains sorting values. The dictionary needs to follow this template :
      - `{'fieldName' : 'ASC', 'fieldName' : 'DESC'}`
    - `limit` (optional)        : Integer that limit how many rows we want to delete.

##### Return
The function returns either True if the delete went well or a pymysql.Error or a pymysql.Warning.

#### Usage :
```python
from models.model import Model
from models.filter import Filter
import pymysql.Error, pymysql.Warning

model = Model("table_name")
filter = Filter(where="`field_name` = 1")

query = model.delete_row(filter=filter)

if isinstance(query, pymysql.Error):
  print("An error occured..")
  print(query)
elif isinstance(query, pymysql.Warning):
  print("Warning")
  print(query)
else:
  print("Rows have been deleted.") # query = True if no errors
```

## About `return_object` parameter 

`query_all_rows(return_object=True)` will return a `QueryAllReturnObject` object.

Both `query_one_row(return_object=True)` and `count_rows(return_object=True)` will return a `QueryOneReturnObject` object.

Here is an exemple how you can interact with `QueryAllReturnObject`'s object returned:

```python
PS D:\pythonProjects\python_CRUD> python
Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>    
>>> from models.model import Model
>>> from models.filter import Filter
>>>
>>> model = Model("auth_permission")
>>>
>>> test = model.query_all_rows(return_object=True)
>>>
>>>
>>> print(type(test))
<class 'models.return_object.QueryAllReturnObject'>
>>>
>>> test.__dict__.keys()
dict_keys(['row_0', 'row_1', 'row_2', 'row_3', 'row_4', 'row_5', 'row_6', 'row_7', 'row_8', 'row_9', 'row_10', 'row_11', 'row_12', 'row_13', 'row_14', 'row_15', 'row_16', 'row_17', 'row_18', 'row_19', 'row_20', 'row_21', 'row_22', 'row_23', 'row_24', 'row_25', 'row_26', 'row_27', 'row_28', 'row_29', 'row_30', 'row_31'])
>>>
>>>
>>> print(test.row_0)
{'id': 1, 'name': 'Can add log entry', 'content_type_id': 1, 'codename': 'add_logentry'}
>>>
>>> print(test.row_0['name'])
Can add log entry
>>>
```

Here is an exemple how you can interact with `QueryOneReturnObject`'s object returned :
```python
PS D:\pythonProjects\python_CRUD> python
Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from models.model import Model
>>> from models.filter import Filter
>>>
>>> model = Model("auth_permission")
>>> filter = Filter(where="`id` = 2")
>>>
>>> test = model.query_one_row(filter=filter, return_object=True)
>>>
>>> test.__dict__.keys()
dict_keys(['id', 'name', 'content_type_id', 'codename'])
>>>
>>> test.id
2
>>>
>>> test.name
'Can change log entry'
>>>
>>> test.content_type_id
1
>>>
>>> test.codename
'change_logentry'
>>>
>>>
>>> test = model.count_rows(return_object=True)
>>>
>>> test.count
32
>>>
```