field_list = ["type", "default", "unique", "not_null", "lens", "choice", "prefix", "max", "min"]
type_list = ["Str", "Int", "Choice", "IP"]  #


class CheckField:
    def start(self, data):
        fields = data['fields']
        rules = data['rules']
        self.field_val(fields, rules)
        self.guid(fields, rules)

        for rk, rv in rules.items():
            for k, v in rv.items():
                getattr(self, k)(rk, k, v)

        return data

    def field_val(self, fields, rules):

        if len(fields) != len(rules):
            raise KeyError('The number of fields and the number of rules do not match')
        for fk, fv in fields.items():
            name = fv.get('name')
            order = fv.get('order')
            if not isinstance(name, str) or not isinstance(order, int):
                raise KeyError(f"field: {fk} Missing arguments or incorrect types name(str) or order(int).")
            if fk not in rules:
                raise KeyError(f'field {fk} Undefined rule')

    def type(self, field, key, val):
        if val in type_list:
            return
        raise KeyError(f"filed: {field}={key} is {val} Unsupported")

    def default(self, field, key, val):
        if isinstance(val, int):
            return
        raise KeyError(f"filed: {field}={key} value: it should be list index.")

    def unique(self, field, key, val):
        if isinstance(val, bool):
            return
        raise KeyError(f"filed: {field}={key} value: it should be bool")

    def not_null(self, field, key, val):
        if isinstance(val, bool):
            return
        raise KeyError(f"filed: {field}={key} value: it should be bool")

    def prefix(self, field, key, val):
        if isinstance(val, str) and len(val) != 0:
            return
        raise KeyError(f"filed: {field}={key} value: it should be srt and lens not 0")

    def choice(self, field, key, val):
        if isinstance(val, list) and len(val) > 2:
            return
        raise KeyError(f"filed: {field}={key} value: it should be list and lens Not less than 2")

    def lens(self, field, key, val):
        if isinstance(val, int) and val != 0:
            return
        raise KeyError(f"filed: {field}={key} value: it should be int and lens not 0")

    def max(self, field, key, val):
        if isinstance(val, int):
            return

        raise KeyError(f"filed: {field}={key} value: it should be int ")

    def min(self, field, key, val):
        if isinstance(val, int) and val != 0:
            return
        raise KeyError(f"filed: {field}={key} value: it should be int")

    def guid(self, fields, rules):
        count = 0
        for fk, fv in fields.items():
            if fv.get('guid'):
                count += 1
        if count != 1:
            raise KeyError('No globally unique identifiers exist or multiple globally unique identifiers appear')


def check_field(data):
    return CheckField().start(data)

