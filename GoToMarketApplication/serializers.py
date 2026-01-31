from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator



class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Account Already Created from This E-mail !",
            )
        ],
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
            "username": {"error_messages": {"unique": "Username Already Exists!"}}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
    