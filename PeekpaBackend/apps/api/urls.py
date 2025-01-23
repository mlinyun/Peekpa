from django.urls import path
from apps.api.view_auth import LoginView, LoginAdminView, RegisterUserView, UserAdminView, UserAdminDetailView, \
    CompanyAdminView
from apps.api.view_job import ResumeView, AvatarView
from apps.api.view_manage import ManageJobListView, ManageJobNameListView, ManageJobDetailView, ManageInterviewListView, \
    ManageInterviewDetailView, ManageInvitationView, ManageInvitationDetailView, DashboardView

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
    # 公司列表接口
    path("manage/company/", CompanyAdminView.as_view(), name="company_admin"),
    # 职位管理接口
    path("manage/job/", ManageJobListView.as_view(), name="manage_job_list_view"),
    # 职位名称列表接口
    path("manage/job/list/", ManageJobNameListView.as_view(), name="manage_job_name_list_view"),
    # 职位详情接口
    path("manage/job/<str:id>/", ManageJobDetailView.as_view(), name="manage_job_detail_view"),
    # 面试列表接口
    path("manage/job/<str:id>/interviews/", ManageInterviewListView.as_view(), name="manage_job_interview_list_view"),
    # 面试详情接口
    path("manage/job/<str:id>/interviews/<str:iid>/", ManageInterviewDetailView.as_view(),
         name="manage_job_interview_detail_view"),
    # 消息创建接口
    path("manage/job/<str:id>/interviews/<str:iid>/invitation/", ManageInvitationView.as_view(),
         name="manage_job_interview_invitation_view"),
    # 消息修改接口
    path("manage/job/<str:id>/interviews/<str:iid>/invitation/<str:ivid>/", ManageInvitationDetailView.as_view(),
         name="manage_job_interview_invitation_detail_view"),
    # 首页数据接口
    path("manage/dashboard/", DashboardView.as_view(), name="dashboard_view"),
]
