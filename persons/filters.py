import django_filters
from .models import Client


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Client
        fields = ["name", "email"]
