from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.api.serializers import LoginSerializer, RegisterUserSerializer, AdminUserListSerializer
from apps.peekpauser.models import User
from apps.api.permissions import IsCompanyAdminUser


class LoginBaseView(generics.GenericAPIView):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = self.queryset.filter(email=email)
        # 用户不存在
        if not user.count():
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 系统登录用户
        auth_user = auth.authenticate(email=email, password=password, is_active=True)
        if auth_user:
            # 更新用户最后登录时间
            update_last_login(None, auth_user)
            return Response(self.get_serializer(auth_user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LoginView(LoginBaseView):
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_staff=False)


class LoginAdminView(LoginBaseView):
    serializer_class = LoginSerializer
    queryset = User.objects.filter(is_staff=True)


class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(LoginSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListFilter(filters.FilterSet):
    q = filters.CharFilter(method="my_custom_filter", label="Search")

    class Meta:
        model = User
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__contains=value) | Q(last_name__contains=value) | Q(email__contains=value)
        )


class UserAdminView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserListFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.user.details.get("company_id", -1)
        queryset = queryset.filter(details__contains={"company_id": company_id}).exclude(uid=self.request.user.uid)
        return queryset

    def perform_create(self, serializer):
        password = self.request.data.get("password")
        user = serializer.save()
        company_id = self.request.user.details.get("company_id")
        details = {
            "company_id": company_id,
            "is_manager": False
        }
        user.details = details
        user.is_staff = True
        user.set_password(password)
        user.save()


class UserAdminDetailView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCompanyAdminUser]
    lookup_field = "uid"

    def get_object(self):
        queryset = super().get_queryset()
        company_id = self.request.user.details.get("company_id", -1)
        queryset = queryset.filter(
            Q(details__contains={"company_id": company_id}))
        uid = self.kwargs["uid"]
        obj = get_object_or_404(queryset, uid=uid)
        return obj

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
