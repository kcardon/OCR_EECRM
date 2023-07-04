from .models import Client, Employee, Group
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ValidationError,
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeSignUpSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "groups",
            "phone",
            "mobile",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise ValidationError("Cet email est déjà enregistré")
        return value

    def create(self, validated_data):
        group_id = validated_data["groups"]
        employee = Employee.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            mobile=validated_data["mobile"],
        )
        employee.groups.set(group_id)
        return employee


class EmployeeLoginSerializer(Serializer):
    username = CharField()
    password = CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            employee = Employee.objects.get(username=username)
        except Employee.DoesNotExist:
            raise ValidationError(
                "Un utilisateur avec ce nom d'utilisateur et ce mot de passe n'a pas été trouvé."
            )

        if not check_password(password, employee.password):
            raise ValidationError("Le mot de passe est incorrect")

        attrs["employee"] = employee
        return attrs
