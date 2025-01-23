from django.urls import path
from apps.api.view_auth import LoginView, LoginAdminView, RegisterUserView, UserAdminView, UserAdminDetailView
from apps.api.view_job import ResumeView, AvatarView

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
    # 简历上传接口
    path("resume/upload/", ResumeView.as_view(), name="resume_upload"),
    # 头像上传接口
    path("avatar/upload/", AvatarView.as_view(), name="avatar_upload"),
    # 公司员工修改接口
    path("manage/user/<str:uid>/", UserAdminDetailView.as_view(), name="user_admin_detail"),
]
