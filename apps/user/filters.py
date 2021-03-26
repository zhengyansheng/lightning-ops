from .models import Organization
from .models import UserProfile

import django_filters


class OrganizationFilter(django_filters.FilterSet):
    pk = django_filters.Filter(method='filter_user_list_handle')

    def filter_user_list_handle(self, qs, name, value):
        """
            pk=<id>
            基于pk查询用户列表
        """
        instance = qs.filter(pk=value)
        query_set = instance.get_descendants(include_self=True)
        u_ids = []
        for q in query_set:
            _qs = q.userprofile_set.all()
            if not _qs:
                continue
            u_ids.extend([u.pk for u in _qs])
        print(UserProfile.objects.filter(pk__in=u_ids))
        return UserProfile.objects.filter(pk__in=u_ids)