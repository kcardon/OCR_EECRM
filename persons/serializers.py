from .models import Client, Employee, Group
from rest_framework.serializers import Serializer, ModelSerializer, CharField,ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class GroupSerializer(ModelSerializer):
    class Meta:
        model=Group
        fields = '__all__'

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'



class EmployeeSignUpSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'group', 'phone', 'mobile')
        extra_kwargs = {'password': {'write_only': True}}
    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise ValidationError("Cet email est déjà enregistré")
        return value
    def create(self, validated_data):
        employee = Employee.objects.create_user(**validated_data)
        return employee


class EmployeeLoginSerializer(Serializer):
    username = CharField()
    password = CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            employee = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

            if not employee:
                msg = _('Unable to authenticate with provided credentials')
                raise ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise ValidationError(msg, code='authorization')

        attrs['user'] = employee
        return attrs
