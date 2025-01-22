from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from shortuuidfield import ShortUUIDField


# Create your models here.
class PeekpaUserManager(BaseUserManager):
    """
    自定义用户管理器类，继承自 BaseUserManager。

    该类定义了创建不同类型用户的方法，包括普通用户、公司人员用户和超级管理员用户。

    方法:
        - create_user(email, password): 创建求职者用户
        - create_admin_user(email, password): 创建公司人员用户
        - create_superuser(email, password): 创建系统超级管理员用户
    """

    def create_user(self, email, password):
        """创建求职者用户"""
        if not email:
            raise ValueError("邮箱格式不正确.")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, email, password):
        """创建公司人员用户"""
        if not email:
            raise ValueError("邮箱格式不正确.")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """创建系统超级管理员用户"""
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    用户模型类，继承自 AbstractBaseUser 和 PermissionsMixin。

    该类定义了用户的基本信息和行为，包括用户的唯一标识、邮箱、姓名、性别、详细信息、状态等。
    同时，使用自定义的用户管理器 PeekpaUserManager 来管理用户的创建和管理操作。

    属性:
        - GENDER_UNKNOWN (int): 性别未知的常量值
        - GENDER_MALE (int): 性别为男性的常量值
        - GENDER_FEMALE (int): 性别为女性的常量值
        - GENDER_ITEMS (tuple): 性别选项的元组，用于性别字段的选择
        - uid (ShortUUIDField): 用户的唯一标识符，主键
        - email (EmailField): 用户的邮箱，唯一且必填
        - first_name (CharField): 用户的姓
        - last_name (CharField): 用户的名
        - gender (PositiveIntegerField): 用户的性别，默认值为 GENDER_UNKNOWN
        - details (JSONField): 用户的详细信息，默认为空字典
        - is_active (BooleanField): 用户是否可以登录，默认值为 True
        - is_staff (BooleanField): 用户是否是公司人员，默认值为 False
        - is_superuser (BooleanField): 用户是否是系统超级管理员，默认值为 False
        - data_join (DateTimeField): 用户加入时间，自动设置为当前时间
        - last_login (DateTimeField): 用户最后登录时间，自动更新为当前时间

    方法:
        name: 返回用户的全名。
    """

    # 定义性别常量
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2

    # 定义性别选项，用于性别字段
    GENDER_ITEMS = (
        (GENDER_MALE, "男"),
        (GENDER_FEMALE, "女"),
        (GENDER_UNKNOWN, "未知")
    )

    # 定义用户模型的字段
    uid = ShortUUIDField(primary_key=True, unique=True)  # 用户主键
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)  # 用户邮箱
    first_name = models.CharField(max_length=30)  # 用户的姓
    last_name = models.CharField(max_length=30)  # 用户的名
    gender = models.PositiveIntegerField(default=GENDER_UNKNOWN, choices=GENDER_ITEMS)  # 用户的性别
    details = models.JSONField(default=dict)  # 用户的详细信息
    is_active = models.BooleanField(default=True)  # 用户是否可以登录
    is_staff = models.BooleanField(default=False)  # 用户是否是公司人员
    is_superuser = models.BooleanField(default=False)  # 用户是否是系统超级管理员
    data_join = models.DateTimeField(verbose_name="data join", auto_now_add=True)  # 用户加入时间
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)  # 用户最后登录时间

    objects = PeekpaUserManager()  # 使用自定义的用户管理器

    # 定义用户的唯一标识字段，这里使用 email 字段作为唯一标识
    USERNAME_FIELD = "email"
    # 定义创建用户时必须填写的字段，这里我们填空
    REQUIRED_FIELDS = []

    @property
    def name(self):
        """返回用户的全名"""
        return "{} {}".format(self.last_name, self.first_name)
