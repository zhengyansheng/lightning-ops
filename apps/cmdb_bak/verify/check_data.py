from ..verify import get_instance
from .operate import OperateInstance


class CheckData:
    def __init__(self, data):
        self.data = data

    def create(self):
        n_data = self.data
        data_map_obj = OperateInstance.get_table_field(n_data['table_classify'])
        data_field = data_map_obj.fields
        field_rule = data_map_obj.rules

        self.field_exist(n_data['data'], data_field)

        for field, rule in field_rule.items():
            for k, v in list(rule.items()):
                if hasattr(self, k):
                    n_data['data'][field] = getattr(self, k)(n_data['table_classify'], field, rule,
                                                             n_data['data'].get(field))
                    rule.pop(k)
            n_data['data'][field] = get_instance(field, rule.pop('type'),
                                                 **rule).stringify(n_data['data'].get(field))
        return n_data

    def unique(self, c_id, field, meta, val):
        if meta['unique']:
            asset_obj_all = OperateInstance.get_all_asset(c_id)
            if not asset_obj_all:
                return val
            for i in asset_obj_all:
                if i.data[field] == val:
                    raise ValueError(f"field {field} value:({val}) already existed.")
        return val

    def not_null(self, c_id, field, meta, val):
        if meta['not_null'] == True and val == None or val == "":
            raise ValueError(f"field {field} nullable={meta['not_null']}, The value passed is not valid. ")
        else:
            return val

    def default(self, c_id, field, meta, val):
        if val == None or val == "":
            return meta['default']
        return val

    def field_exist(self, new_value_dic, field_dic):
        for k, v in new_value_dic.items():
            if k in field_dic:
                continue
            else:
                raise ValueError(f'field {k} Is not defined')


def check_data(data, model):
    check_inc = CheckData(data)
    return getattr(check_inc, model)()
