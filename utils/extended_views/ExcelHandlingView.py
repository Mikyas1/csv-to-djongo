import time
from accounts import models
from utils.extended_models.ExtendedModel import ModelWithCreateFromDict


class ExcelHandlingView:

    @classmethod
    def isNaN(cls, num):
        return num != num

    @classmethod
    def get_value_or_none(cls, val):
        if cls.isNaN(val):
            return None
        return str(val).strip()

    @classmethod
    def get_excel_fields(cls, dict):
        res = []
        for v in dict.values():
            res.append(v)
        return res

    @classmethod
    def can_model_handle_ExcelHandlingView(cls, model):
        if not hasattr(model, 'excel_titles'):
            raise Exception(
                "`BY MIKE` := {} has got no excel_titles defined".format(model))
        if not hasattr(model, 'create_obj_form_dict'):
            raise Exception("`BY MIKE` := {} is not a child of {}".format(
                model, ModelWithCreateFromDict))

    @classmethod
    def create_model_object(cls, model, row, other_dict_data={}):
        # cls.delete_every_recore_on_that_model(model)
        data = other_dict_data
        for d in model.excel_titles:
            data[d] = cls.get_value_or_none(row.get(model.excel_titles[d]))
        return model.create_obj_form_dict(data)

    @classmethod
    def delete_every_recore_on_that_model(cls, model):
        model.objects.all().delete()

    @classmethod
    def delete_every_record_that_match_criteria(cls, model, filter):
        print("got here")
        print(filter)
        model.objects.filter(**filter).delete()
