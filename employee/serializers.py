from rest_framework import serializers
from employee.models import User
from rest_framework.validators import UniqueValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    user_number = serializers.IntegerField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all()),
        MaxValueValidator(9999),
        MinValueValidator(1000),
    ])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('user_number', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            user_number=validated_data['user_number'],
            role=validated_data['role'],
        )
        if validated_data['role'] == 'Admin':
            user.is_admin = True
            user.is_superuser = True
            user.is_staff = True

        user.set_password(validated_data['password'])
        user.save()

        return user
