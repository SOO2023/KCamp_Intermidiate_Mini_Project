#a simple int id generator
def id_gen (dict_obj):
    keys = list(dict_obj.keys())
    if len(keys) != 0:
        last_id = list(dict_obj.keys())[-1]
        return last_id + 1
    else:
        return 1