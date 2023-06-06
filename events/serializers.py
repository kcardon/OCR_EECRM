from rest_framework import serializers
from .models import Event, EventStatus
from contracts.models import Contract
from persons.models import Client, Employee


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = ['id', 'status']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    
    client = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Client.objects.all()
    )

    contract = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Contract.objects.all()
    )

    event_status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset =EventStatus.objects.all()
    )