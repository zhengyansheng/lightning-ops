from .operate import OperateInstance
from ..verify import get_instance


class CheckData:
    def __init__(self, data, instance):
        self.data = data
        self.data_filed_obj = OperateInstance.get_table_field(data['table_classify'])
        self.data_field = self.data_filed_obj.fields
        self.field_rule = self.data_filed_obj.rules
        self.instance = instance

    def run(self):
        # 判断提交上来的字段 是否对应 表定义字段
        self.field_exist(self.instance, self.data['data'], self.data_field)

        # 校验通用字段
        for field, rule in self.field_rule.items():
            for k, v in list(rule.items()):
                if hasattr(self, k):
                    self.data['data'][field] = getattr(self, k)(self.instance, self.data['table_classify'], field, rule,
                                                                self.data['data'].get(field))
                    rule.pop(k)

            # 校验 type
            self.data['data'][field] = get_instance(field, rule.pop('type'),
                                                    **rule).stringify(self.data['data'].get(field))
        return self.data

    def unique(self, instance, c_id, field, meta, val):
        if meta['unique']:
            asset_obj_all = OperateInstance.get_all_asset(c_id)
            if not asset_obj_all:
                return val
            for i in asset_obj_all:
                if instance and instance.id == i.id:
                    continue
                if i.data[field] == val:
                    raise ValueError(f"field {field} value:({val}) already existed.")
        return val

    def not_null(self, instance, c_id, field, meta, val):
        if meta['not_null'] == True and val == None or val == "":
            raise ValueError(f"field {field} nullable={meta['not_null']}, The value passed is not valid. ")
        else:
            return val

    def default(self, instance, c_id, field, meta, val):
        if val == None or val == "":
            return meta['default']
        return val

    def field_exist(self, instance, new_value_dic, field_dic):
        for k, v in new_value_dic.items():
            if k in field_dic:
                continue
            else:
                raise ValueError(f'field {k} Is not defined')


def check_data(data, instance):
    return CheckData(data, instance).run()
