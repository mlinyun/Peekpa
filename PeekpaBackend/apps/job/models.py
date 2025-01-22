from datetime import timedelta
from django.db import models
from django.db.models import F
from django.utils import timezone
from apps.company.models import Company
from apps.peekpauser.models import User


# Create your models here.
class Resume(models.Model):
    """简历模型类"""
    id = models.AutoField(primary_key=True)  # 简历 ID，主键
    name = models.CharField(max_length=200)  # 简历名称
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume")  # 简历所属用户，外键，和系统用户关联
    url = models.URLField()  # 简历文件 URL
    is_active = models.BooleanField(default=True)  # 当前简历是否是使用中的简历


class Job(models.Model):
    """职位模型类"""
    STATUS_PUBLISH = 0  # 职位状态：已发布
    STATUS_CLOSE = 1  # 职位状态：已下线
    STATUS_FINISH = 2  # 职位状态：已结束
    # 职位状态选项
    STATUS_ITEMS = (
        (STATUS_PUBLISH, "已发布"),
        (STATUS_CLOSE, "已下线"),
        (STATUS_FINISH, "已结束"),
    )

    id = models.AutoField(primary_key=True)  # 职位 ID，主键
    title = models.CharField(max_length=100)  # 职位名称
    status = models.PositiveIntegerField(default=STATUS_PUBLISH, choices=STATUS_ITEMS)  # 职位状态
    city = models.CharField(max_length=10, null=True)  # 职位所在城市
    location = models.CharField(max_length=50, null=True)  # 职位详细地址
    salary_min = models.PositiveIntegerField(default=0)  # 职位月薪最小值
    salary_max = models.PositiveIntegerField(default=0)  # 职位月薪最大值
    salary_count = models.PositiveIntegerField(default=0)  # 职位月薪计数
    hire_number = models.PositiveIntegerField(default=1)  # 职位招聘人数
    experience = models.CharField(max_length=50)  # 职位工作经验要求
    benefit = models.CharField(max_length=300)  # 职位福利待遇
    education = models.CharField(max_length=30)  # 职位学历要求
    description = models.CharField(max_length=3000)  # 职位描述
    publish_time = models.DateTimeField(auto_now_add=True)  # 职位发布时间
    resumes = models.ManyToManyField(Resume)  # 职位收到的简历
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name="jobs")  # 职位所属公司，外键，和公司关联


class PublishJob(models.Model):
    """发布职位模型类（中间表）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 发布职位的用户, 外键，和用户关联，这里的用户仅仅是公司用户
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # 发布的职位，外键，和职位关联


class Interview(models.Model):
    """面试模型类"""
    id = models.AutoField(primary_key=True)  # 面试 ID，主键
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="interviews")  # 面试职位，外键，和职位关联
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interviews")  # 面试者（招聘者）
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_interviews")  # 被面试者（求职者）
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="interviews")  # 面试简历，外键，和简历关联
    status = models.PositiveIntegerField(default=0)  # 当前面试状态
    publish_time = models.DateTimeField(auto_now_add=True)  # 创建面试的时间
    feedback = models.JSONField(default=dict)  # 面试反馈，JSON 格式，包含面试结果和面试评价


class Invitation(models.Model):
    """面试邀请模型类"""
    RESPONSE_UNRESPONSE = 0  # 面试邀请回复：未回复
    RESPONSE_YES = 1  # 面试邀请回复：同意
    RESPONSE_NO = 2  # 面试邀请回复：拒绝
    RESPONSE_CLOUSE = 3  # 面试邀请回复：取消
    # 面试邀请回复选项
    RESPONSE_ITEMS = (
        (RESPONSE_UNRESPONSE, "未回复"),
        (RESPONSE_YES, "同意"),
        (RESPONSE_NO, "拒绝"),
        (RESPONSE_CLOUSE, "取消"),
    )
    id = models.AutoField(primary_key=True)  # 面试邀请 ID，主键
    status = models.PositiveIntegerField(default=0)  # 面试邀请状态
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="invitations")  # 面试邀请
    message = models.CharField(max_length=200)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interview_invitation")  # 面试者
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_invitation")  # 被面试者
    response = models.PositiveIntegerField(default=RESPONSE_UNRESPONSE, choices=RESPONSE_ITEMS)  # 面试邀请回复
    publish_time = models.DateTimeField(auto_now_add=True)  # 创建面试邀请的时间
    update_time = models.DateTimeField(auto_now=True)  # 更新面试邀请的时间
    due_time = models.DateTimeField(default=F("publish_time") + timedelta(days=3))  # 面试邀请的截止时间

    def save(self, *args, **kwargs):
        self.update_time = timezone.now()  # 在保存模型时更新 update_time 字段
        super().save(*args, **kwargs)
