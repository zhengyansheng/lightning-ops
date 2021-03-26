import django_filters


class ServiceTreeFilter(django_filters.FilterSet):
    node = django_filters.Filter(method="node_handle")
    host = django_filters.Filter(method="host_handle")

    def node_handle(self, qs, name, value):
        ids = []
        for instance in qs.filter(name=value):
            ins_ancestor = instance.get_ancestors(ascending=False, include_self=True).values("id")
            ids.extend([x["id"] for x in ins_ancestor])
        return qs.filter(pk__in=ids)

    def host_handle(self, qs, name, value):
        return qs