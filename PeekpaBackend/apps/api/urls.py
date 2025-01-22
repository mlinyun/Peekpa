from django.urls import path
from apps.api.view_auth import LoginView, LoginAdminView, RegisterUserView, UserAdminView

app_name = "api"

urlpatterns = [
    # 求职者用户登录接口
    path("auth/signin/", LoginView.as_view(), name="signin_view"),
    # 求职者用户注册接口
    path("auth/signup/", RegisterUserView.as_view(), name="signup_view"),
    # 公司人员用户登录接口
    path("auth/login/", LoginAdminView.as_view(), name="login_admin"),
    # 公司人员用户注册接口（一般员工注册）
    path("manage/user/", UserAdminView.as_view(), name="user_admin"),
]
