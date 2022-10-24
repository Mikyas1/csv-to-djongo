# CSV to DJONGO/DJANGO

Simple mixin library for handling CSV uploads. It can extract multiple fields, including relational fields (ArrayReferenceField and ForeignKey) Assuming Djongo as ORM.

## VALUE
- Mapping of Excel columns to field names
- Creating ForeignKey - reads foreign key fields and creates and associates them 
from the Excel row directly.
- Creating ArrayReferenceField - reads many-to-many relations and creat and associates them with 
the model.


    Eg: Excel (csv)

    | Name (Char)   | school (Foreign-key)   | course (ArrayReferenceField) |
    | ------------- | ---------------------- | ---------------------------- |
    | Jon           | Coding school          |  java                        |  
    |               |                        |  python                      |

---

## USAGE

### MODELS

Import **ModelWithCreateFromDict** and add it as mixin. Define excel column to field name mapping
using **excel_titles**. Mark important and non-nullable fields using **important_fields**.

```python
from django.db import models
from utils.extended_models.ExtendedModel import ModelWithCreateFromDict

class Student(models.Model, ModelWithCreateFromDict):
    ...
    ...

    excel_titles = {
        "field_name": "column_name"
    }
    
    important_fields = ["field_name"]
    
```

### Views
Import **ExcelHandlingView** and add it as a mixin to you view. Prepare your rows in dict format
(pd.DataFrame from pands), loop over your rows and call **create_model_object** with the model name
the row and any default kwargs.


```python
from rest_framework.views import APIView
from utils.extended_views.ExcelHandlingView import ExcelHandlingView

class YourView(APIView, ExcelHandlingView):
    # get your csv file 
    # use pands or whatever you want to create DataFrames
    # pass each DataFrame row
    
    excel_file = pd.read_excel(file)
        data = pd.DataFrame(
            excel_file, columns=self.get_excel_fields(
                models.Student.excel_titles
            )
        )
    
    for _, row in data.iterrows():
        self.create_model_object(models.Student, row, {"age": 21})

```
