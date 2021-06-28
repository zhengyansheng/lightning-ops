import ipaddress

from apps.cmdb.verify.operate import OperateInstance

classes_cache = {}
instances_cache = {}


# 获取类
def get_class(type):
    cls = classes_cache.get(type)
    if cls:
        return cls
    raise TypeError(f"Wrong Type! {cls} is not BaseType")


# 获取实例对象
def get_instance(type, **option):
    key = ",".join(f"{k}={v}" for k, v in sorted(option.items()))
    key = f"{type}|{key}"
    obj = instances_cache.get(key)
    if obj:
        return obj

    obj = get_class(type)(**option)
    instances_cache[key] = obj
    return obj


class BaseType:
    """base 存放通用属性和 初始化数据"""

    def __init__(self, instance, field, table_classify, **option):
        self.instance = instance
        self.field = field
        self.table_classify = table_classify
        self.option = option

    def __getattr__(self, item):
        return self.option.get(item)

    def field_check(self, value):
        raise NotImplementedError()

    def prefix_func(self, val):
        if not str(val).strip().startswith(self.prefix.strip()):
            raise ValueError(
                f"field {self.field} is {val} not startswith [{self.prefix}]"
            )
        return val

    def suffix_func(self, val):
        if not str(val).strip().endswith(self.suffix.strip()):
            raise ValueError(
                f"field {self.field} is {val} not endswith [{self.suffix}]"
            )
        return val

    def unique_func(self, val):
        asset_obj_all = OperateInstance.get_all_asset(self.table_classify)
        if not asset_obj_all:
            return val
        for i in asset_obj_all:
            if self.instance and self.instance.id == i.id:
                continue
            elif i.data[self.field] == val:
                raise ValueError(f"field {self.field} value:({val}) already existed.")

        return val

    def not_null_func(self, val):
        print(val)
        print(11111111111)
        if self.not_null and not val or val == "":
            raise ValueError(
                f"field {self.field} nullable={self.not_null}, The value passed is not valid. "
            )
        else:
            return val

    def default_func(self, val):
        if not val or val == "":
            return self.default
        return val

    def data_check(self, val):
        for k, v in self.__dict__["option"].items():
            if hasattr(self, f"{k}_func"):
                val = getattr(self, f"{k}_func")(val)
        return val


# globals() 函数会以字典类型返回当前位置的全部全局变量。
def init_class():
    for n, t in globals().items():
        if type(t) == type and issubclass(t, BaseType) and n != "BaseType":
            classes_cache[n] = t
            classes_cache[f"{__name__}.{n}"] = t


class Int(BaseType):
    def data_check(self, val):
        if val:
            return super(Int, self).data_check(int(val))
        return super(Int, self).data_check(val)

    def max_func(self, val):
        val = int(val)
        max = self.max
        if max and val != 0 and val > max:
            raise ValueError(
                f"field {self.field} Too big value to {val} Limited to {max}"
            )
        return int(val)

    def min_func(self, val):
        val = int(val)
        min = self.min
        if max and val != 0 and val < min:
            raise ValueError(
                f"field {self.field} Too small value is {val} Limited to {min}"
            )
        return int(val)


class Str(BaseType):
    def data_check(self, val):
        if val:
            return super(Str, self).data_check(str(val))
        return super(Str, self).data_check(val)

    def lens_func(self, val):
        len_num = self.lens
        if val:
            if len(val) > int(len_num):
                raise ValueError(
                    f"field {self.field} is {val} Out of length limit, should be less than  {len_num}"
                )
        return val


class IP(BaseType):
    def data_check(self, val):
        if val:
            return super(IP, self).data_check(str(ipaddress.ip_address(val)))
        return super(IP, self).data_check(str(val))


class Choices(BaseType):
    def data_check(self, val):
        if val:
            return super(Choices, self).data_check(str(val))
        return super(Choices, self).data_check(val)

    def select_list_func(self, val):
        if val:
            if val in self.select_list:
                return val
            else:
                raise ValueError(
                    f"The specified value {val} is not in the optional list:{self.select_list}"
                )
        return val


def check_data(data, instance):
    data_filed_obj = OperateInstance.get_table_field(data["table_classify"])
    print(data)
    field_rule = data_filed_obj.rules
    for field, rule in field_rule.items():
        print(field)
        rule["field"] = field
        rule["table_classify"] = data["table_classify"]
        rule["instance"] = instance
        data["data"][field] = get_instance(rule.pop("type"), **rule).data_check(
            data["data"].get(field.strip())
        )
    return data


init_class()
