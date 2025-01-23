from rest_framework import serializers
from apps.company.models import Company
from apps.job.models import Resume
from apps.peekpauser.models import User, Avatar


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6, write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "token"]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email, password)
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.save()
        return user


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "first_name", "last_name", "gender", "data_join", "last_login", "is_active"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"


class AdminCompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "first_name", "last_name", "data_join"]


class AdminCompanyListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    email = serializers.CharField(write_only=True, read_only=False)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def get_user(self, obj):
        user = User.objects.filter(details__contains={"company_id": obj.id, "is_manager": True})
        if user.count():
            return AdminCompanyUserSerializer(user.all().first()).data
        return None

    class Meta:
        model = Company
        fields = ["id", "name", "website", "user", "email", "first_name", "last_name", "password"]
