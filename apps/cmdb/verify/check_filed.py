import copy

field_list = [
    "type",
    "default",
    "unique",
    "not_null",
    "lens",
    "choice",
    "prefix",
    "max",
    "min",
]
type_list = ["Str", "int", "Choice", "IP"]  #

classes_cache = {}
instances_cache = {}


# 获取类
def get_class(type):
    cls = classes_cache.get(type)
    if cls:
        return cls
    raise TypeError(f"Wrong Type! {cls} is not BaseType")


# 获取实例对象
def get_instance(type, field, **field_rule):
    key = ",".join(f"{k}={v}" for k, v in sorted(field_rule.items()))
    key = f"{type}|{key}"
    obj = instances_cache.get(key)
    if obj:
        return obj

    obj = get_class(type)(field, **field_rule)
    instances_cache[key] = obj
    return obj


class BaseType:
    def __init__(self, fields, **data):
        self.fields = fields
        self.data = data

    def field_check(self):
        if "order" not in self.__dict__["data"]:
            raise KeyError(f"{self.fields} The [order] field must exist")
        if "name" not in self.__dict__["data"]:
            raise KeyError(f"{self.fields} The [name] field must exist")

        for k, v in self.__dict__["data"].items():
            if hasattr(self, f"{k}_func"):
                getattr(self, f"{k}_func")(v)
            else:
                pass

    def unique_func(self, v):
        if not isinstance(v, bool):
            raise KeyError(f"{self.fields}: [unique] Only bool types are supported")

    def name_func(self, v):
        if not isinstance(v, str):
            raise KeyError(f"{self.fields}: [name] Only str types are supported")

    def order_func(self, v):
        if not isinstance(v, int):
            raise KeyError(f"{self.fields}: [order] Only int types are supported")

    def default_func(self, val):
        if "select_list" in self.__dict__["data"]:
            if val not in self.__dict__["data"]["select_list"]:
                raise KeyError(
                    f"{self.fields}: type [Choices][default] Must be the value in the select_list "
                )

        if len(val) == 0:
            raise KeyError(f"{self.fields}: [default] value: can not be empty.")

    def not_null_func(self, val):
        if not isinstance(val, bool):
            raise KeyError(f"{self.fields}: [not_null] Only bool types are supported")

    def prefix_func(self, val):
        if isinstance(val, str) and len(val) == 0:
            raise KeyError(
                f"{self.fields}: [prefix]  value: it should be srt and lens is 0"
            )

    def suffix_func(self, val):
        if isinstance(val, str) and len(val) == 0:
            raise KeyError(
                f"{self.fields}: [suffix]  value: it should be srt and lens is 0"
            )

    def guid(
        self,
    ):
        count = 0
        for fk, fv in self.fields.items():
            if fv.get("guid"):
                count += 1
        if count != 1:
            raise KeyError(
                "No globally unique identifiers exist or multiple globally unique identifiers appear"
            )


# globals() 函数会以字典类型返回当前位置的全部全局变量。
def init_class():
    for n, t in globals().items():
        if type(t) == type and issubclass(t, BaseType) and n != "BaseType":
            classes_cache[n] = t
            classes_cache[f"{__name__}.{n}"] = t


class IntFunc(BaseType):
    def max_func(self, v):
        if not isinstance(v, int):
            raise KeyError(f"{self.fields}: [max] Only int types are supported")

    def min_func(self, v):
        if not isinstance(v, int):
            raise KeyError(f"{self.fields}: [min] Only int types are supported")


class StrFunc(BaseType):
    def lens_func(self, v):
        if not isinstance(int(v), int):
            raise KeyError(f"{self.fields}: [lens] Only int types are supported")


class IPFunc(BaseType):
    pass


class ChoicesFunc(BaseType):
    def field_check(self):
        if "select_list" not in self.__dict__["data"]:
            raise KeyError(
                f"{self.fields},[Choices] type: There must be a select_list "
            )
        super(ChoicesFunc, self).field_check()

    def select_list_func(self, v):
        if not isinstance(v, list) or len(v) < 0:
            raise KeyError(
                f"{self.fields}: [select_list] Only list types are supported or Quantity less than zero "
            )


def check_field(data):
    data = copy.deepcopy(data)
    guid_num = 0
    for k, v in data["fields"].items():
        types = data["rules"][k].pop("type")
        data["rules"][k].update(v)
        guid = v.pop("guid")
        if guid:
            guid_num += 1
            if guid_num != 1:
                raise KeyError(f"[guid]: There can only be one")
        get_instance(f"{types}Func", k, **data["rules"][k]).field_check()
    if guid_num != 1:
        KeyError(f"[guid]: There can only be one")


init_class()
