from utils.extended_models import helpers
class ModelWithCreateFromDict:


    @classmethod
    def all_important_fields_are_provided(cls, dict):
        if not hasattr(cls, 'important_fields'): return
        res = True
        for field in getattr(cls, 'important_fields'):
            if dict.get(field) == None or dict.get(field) == "": 
                # raise Exception("`BY MIKE` := `{}` is important field and not been provided".format(field))
                print("`BY MIKE` := `{}` is important field and not been provided".format(field))
                res = False
        return res
        
    @classmethod
    def create_obj_form_dict(cls, dict):

        data = {}
        arr_data = {}

        # This has side effect it might create objects on db if 
        # it can't get them `create_object_with_name` method
        for val in dict:
            try:
                field = cls._meta.get_field(val)
                field_type = field.get_internal_type()

                if field_type != "ArrayReferenceField" and field_type != "ForeignKey":
                    data[val] = dict[val]
                elif field_type == "ForeignKey":
                    data[val] = helpers.get_or_create_foreignkey_object_by_name_or_id(
                        field.related_model, dict[val]
                    )
                elif field_type == "ArrayReferenceField":
                    arr_data[val] = helpers.get_array_objects_by_name(
                        field.related_model, dict[val]
                    )
                    # ADD CASE FOR `ArrayField`
            except Exception as e:
                print(e)
        
        if not cls.all_important_fields_are_provided(data):
            # NOTE if all important fields are not on dict ignore that row
            return

        try:
            obj = cls.objects.create(**data)
            for ad in arr_data:
                many_to_many_field = getattr(obj, ad)
                for arr_val in arr_data[ad]:
                    many_to_many_field.add(arr_val)

            return obj
        except Exception as e:
            # NOTE if DB object is not able to be created from dict for some reason ignore that dict
            print(e)
            return None
