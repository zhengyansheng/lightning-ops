import django_filters


class CmdbFilter(django_filters.FilterSet):
    hostname = django_filters.Filter(method="hostname_handle")
    private_ip = django_filters.Filter(method="private_ip_handle")

    def hostname_handle(self, qs, name, value):
        return qs.filter(hostname=value)

    def private_ip_handle(self, qs, name, value):
        return qs.filter(private_ip=value)