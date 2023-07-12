# filters.py
import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(
        field_name="client__last_name", lookup_expr="icontains"
    )
    client_email = django_filters.CharFilter(
        field_name="client__email", lookup_expr="icontains"
    )
    date_before = django_filters.DateFilter(
        field_name="event_date", lookup_expr="lte"
    )  # less or equal
    date_after = django_filters.DateFilter(
        field_name="event_date", lookup_expr="gte"
    )  # greater or equal

    class Meta:
        model = Event
        fields = ["client_name", "client_email", "date_before", "date_after"]
