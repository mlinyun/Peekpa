from django.urls import path
from apps.api.view_auth import LoginView, LoginAdminView, RegisterUserView, UserAdminView, UserAdminDetailView, \
    CompanyAdminView
from apps.api.view_job import ResumeView, AvatarView, JobListView, JobDetailView, InvitationDetailView, ApplyJobView
from apps.api.view_manage import ManageJobListView, ManageJobNameListView, ManageJobDetailView, ManageInterviewListView, \
    ManageInterviewDetailView, ManageInvitationView, ManageInvitationDetailView, DashboardView
from apps.api.view_company import CompanyListView, CompanyDetailView

from apps.api.view_index import IndexView

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
    # 招聘网站前端职位列表接口
    path("job/", JobListView.as_view(), name="job_list_view"),
    # 招聘网站前端职位详情接口
    path("job/<str:id>/", JobDetailView.as_view(), name="job_detail_view"),
    # 回复面试邀请消息接口
    path("invitation/<str:iid>/", InvitationDetailView.as_view(), name="invitation_detail_view"),
    # 职位申请接口
    path("job/<str:id>/apply/", ApplyJobView.as_view(), name="apply_job_view"),
    # 公司列表接口
    path("company/", CompanyListView.as_view(), name="company_list_view"),
    # 公司详情接口
    path("company/<str:id>/", CompanyDetailView.as_view(), name="company_detail_view"),
    # 首页接口初始化
    path("index/", IndexView.as_view(), name="index_view"),
]
