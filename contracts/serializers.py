from rest_framework import serializers
from .models import Contract, ContractStatus
from persons.models import Client, Employee


class ContractStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = ['id', 'status']

class ContractSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contract
        fields = '__all__'

    sales_contact = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Employee.objects.all() 
    )

    client = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Client.objects.all()
    )

    status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ContractStatus.objects.all()
    )

