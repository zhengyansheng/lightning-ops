import importlib
import ipaddress

classes_cache = {}
instances_cache = {}


def get_class(type):
    cls = classes_cache.get(type)
    if cls:
        return cls

    raise TypeError(f'Wrong Type! {cls} is not BaseType')


def get_instance(field, type, **option):
    key = ",".join(f"{k}={v}" for k, v in sorted(option.items()))
    key = f"{type}|{key}"

    obj = instances_cache.get(key)
    if obj:
        return obj

    obj = get_class(type)(field, **option)
    instances_cache[key] = obj

    return obj


def inject():
    for n, t in globals().items():
        if type(t) == type and issubclass(t, BaseType) and n != 'BaseType':
            classes_cache[n] = t
            classes_cache[f"{__name__}.{n}"] = t


class BaseType:
    def __init__(self, field, **option):
        self.field = field
        self.option = option

    def __getattr__(self, item):
        return self.option.get(item)

    def stringify(self, value):
        raise NotImplementedError()

    def prefix_func(self, prefix, val, value):
        if not str(val).startswith(prefix):
            raise ValueError(f'field {self.field} is {value} not startswith {prefix}')
        return str(ipaddress.ip_address(value))


class Int(BaseType):
    def stringify(self, value):
        val = int(value)
        max = self.max
        if max and val != 0 and val > max:
            raise ValueError(f'field {self.field} Too big value to {value} Limited to {max}')
        min = self.min
        if max and val != 0 and val < min:
            raise ValueError(f'field {self.field} Too small value is {value} Limited to {min}')
        return val

    def destringify(self, value):
        return value


class IP(BaseType):
    def stringify(self, value):
        val = value
        prefix = self.prefix
        if val:
            if self.prefix:
                self.prefix(self.prefix())
            if prefix and not str(val).startswith(prefix):
                raise ValueError(f'field {self.field} is {value} not startswith {prefix}')
            return str(ipaddress.ip_address(value))
        return val

    def destringify(self, value):
        return value


class Str(BaseType):
    def stringify(self, value):
        len_num = self.length
        if len_num and len(value) > len_num:
            raise ValueError(f'field {self.field} is {value} Out of length limit, should be less than  {len_num}')
        return str(value)

    def destringify(self, value):
        return value


class Choice(BaseType):
    def stringify(self, value):
        if len(self.choice) < value:
            raise ValueError(f'field {self.field} Choice value:({value}) Out of maximum index')
        return value

    def destringify(self, value):
        return value


inject()
