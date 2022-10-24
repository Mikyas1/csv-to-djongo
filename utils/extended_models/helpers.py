from django.core.exceptions import FieldDoesNotExist

def get_or_create_foreignkey_object_by_name_or_id(model, name):
  dict = prepare_name_or_id_for_model_as_dict(model, name)
  try:
    obj = model.objects.get(**dict)
    return obj
  except model.DoesNotExist:
    return create_object_with_name(model, dict)
  except Exception as e:
    raise Exception(e)


def get_array_objects_by_name(model, name):
  ret = []
  if name == None:
    return ret
  names = name.split(",")
  for nm in names:
    preped_name = nm.strip().lower()
    try:
      obj = model.objects.get(name=preped_name)
      ret.append(obj)
    except model.DoesNotExist:
      new_obj = create_object_with_name(model, {"name": preped_name})
      if new_obj != None:
        ret.append(new_obj)
    except Exception as e:
      pass
  return ret

def create_object_with_name(model, dict):
  object = None
  try:
    object = model.objects.create(**dict)
  except Exception as e:
    print(e)
  return object

def prepare_name_or_id_for_model_as_dict(model, val) -> "dict[str, str]":
  dict = {}
  if val == None:
    return dict
  if type(val) == int:
    return {"id": val}
  try:
    model._meta.get_field("name")
    dict["name"] = val.lower()
  except FieldDoesNotExist:
    model._meta.get_field("_name")
    dict["_name"] = val.lower() 
  return dict