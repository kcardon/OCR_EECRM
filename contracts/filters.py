# filters.py
import django_filters
from .models import Contract


class ContractFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(
        field_name="client__last_name", lookup_expr="icontains"
    )
    client_email = django_filters.CharFilter(
        field_name="client__email", lookup_expr="icontains"
    )
    date_before = django_filters.DateFilter(
        field_name="date_created", lookup_expr="lte"
    )  # less or equal
    date_after = django_filters.DateFilter(
        field_name="date_created", lookup_expr="gte"
    )  # greater or equal
    amount_lte = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    amount_gte = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")

    class Meta:
        model = Contract
        fields = [
            "client_name",
            "client_email",
            "date_before",
            "date_after",
            "amount_lte",
            "amount_gte",
        ]
