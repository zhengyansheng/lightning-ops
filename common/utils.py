from inspect import isfunction

from django.db import models


def random_char_list(num, type=1):
    # type 1:纯数字 2:纯小写字母 3:数字+小写字母 4: 数字+小写字母+大写字母
    import random
    if type == 1:
        chars = list(range(10))
    elif type == 2:
        chars = [chr(i) for i in range(97, 123)]
    elif type == 3:
        chars = list(range(10)) + [chr(i) for i in range(97, 123)]
    elif type == 4:
        chars = list(range(10)) + [chr(i) for i in range(65, 91) + range(97, 123)]
    else:
        return []
    return random.sample(chars, num)


# True 第一个表示是否使用默认搜索（所有的select都成为搜索条件）
# True 第二个 是否开启 多选搜索
# 第三个表示 排序  1表示使用 requiredlist值作为show 2。需要调整的放到后边，3,全部显示
# 参数isShow  显示顺序 几种 组合
# m2mList 多选  添加  一般处理多对多 字段
# 参数 forceFields 强制 字段  编辑，查看，v表，只显示这几个 None 无效
def deal_fields_Table(fields, isSearchDef=True, isSearchMulDef=True, isShow=2, m2mList=None, forceFields=None,
                      hiddenFields=None):
    '''
    处理fields 生成 创建前端 table 需要的属性
    '''
    table_dict = {}
    field_dict = {}
    field_select_list = []
    field_select_mul_list = []
    field_select_kv_list = []
    field_textarea_list = []
    field_radio_list = []
    field_datetime_list = []
    field_date_list = []
    field_time_list = []
    field_required_list = []
    field_default_list = []

    for field in fields:
        if forceFields and field.name not in forceFields:
            continue
        # name
        field_dict[field.name] = field.verbose_name

        # type
        if isinstance(field, models.TextField):
            field_textarea_list.append(field.name)
        elif isinstance(field, models.BooleanField):
            field_radio_list.append(field.name)
        elif isinstance(field, models.ForeignKey):
            field_select_list.append(field.name)
        elif isinstance(field, models.ManyToManyField):
            field_select_mul_list.append(field.name)
            field_select_list.append(field.name)

        elif isinstance(field, models.DateTimeField):
            field_datetime_list.append(field.name)
        elif isinstance(field, models.DateField):
            field_date_list.append(field.name)
        elif isinstance(field, models.TimeField):
            field_time_list.append(field.name)

        # select add value lable
        if field.choices and len(field.choices) > 0:
            field_select_list.append(field.name)
            field_select_kv_list.append({field.name: field.choices})

        # valueDefault
        if field.default is not models.fields.NOT_PROVIDED and isfunction(field.default) is False:
            if field.default != -1:
                field_default_list.append({field.name: field.default})

        # required
        if field.blank is False:
            field_required_list.append(field.name)

    # 调整顺序
    if forceFields:
        field_dict_tmp = {}
        table_dict["field_show_order"] = []
        for f in forceFields:
            if f in field_dict:
                field_dict_tmp[f] = field_dict[f]
                table_dict["field_show_order"].append(f)

        table_dict["fields"] = field_dict_tmp

    else:
        table_dict["fields"] = field_dict

    table_dict["field_required"] = field_required_list

    table_dict["field_type"] = {}

    table_dict["field_type"]["select"] = field_select_list
    table_dict["field_type"]["select_mul"] = field_select_mul_list
    table_dict["field_type"]["textarea"] = field_textarea_list
    table_dict["field_type"]["radio"] = field_radio_list
    table_dict["field_type"]["datetime"] = field_datetime_list
    table_dict["field_type"]["date"] = field_date_list
    table_dict["field_type"]["time"] = field_time_list

    table_dict["field_default"] = field_default_list

    table_dict["field_select_kv"] = field_select_kv_list
    table_dict["field_sort"] = ['id']

    table_dict["field_add_remove"] = []
    table_dict["field_update_remove"] = []

    if isSearchDef:
        table_dict["field_search"] = field_select_list + field_radio_list
    if isSearchMulDef:
        table_dict["field_search_mul"] = field_select_mul_list

    table_dict["field_after_order"] = ["create_time", "update_time", "remark"]
    if hiddenFields:
        table_dict["field_hidden"] = ["id", "create_time", "update_time", "remark"] + hiddenFields
    else:
        table_dict["field_hidden"] = ["id", "create_time", "update_time", "remark"]
    # 默认顺序
    if isShow == 1:
        table_dict["field_show_order"] = field_required_list
        field_hidden_list = []
        for key in field_dict:
            if key not in field_required_list:
                field_hidden_list.append(key)
        table_dict["field_hidden"] = field_hidden_list
    # 默认这几个并且没有调整过顺序
    elif isShow == 2:
        if forceFields is None:
            field_show_list = []
            for key in field_dict:
                if key not in table_dict["field_after_order"]:
                    field_show_list.append(key)
            table_dict["field_show_order"] = field_show_list
    # all 显示所有
    elif isShow == 3:
        field_show_list = []
        for key in field_dict:
            field_show_list.append(key)
        table_dict["field_show_order"] = field_show_list
        table_dict["field_hidden"] = []

    # 多选
    table_dict['field_add_novis'] = []

    return table_dict

