from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.AutoField(primary_key=True)  # 公司 ID，主键
    avatar = models.URLField()  # 公司 Logo
    name = models.CharField(max_length=100)  # 公司名称
    slogan = models.CharField(max_length=100)  # 公司口号
    tags = models.CharField(max_length=100)  # 公司标签
    size = models.CharField(max_length=100)  # 公司规模
    website = models.URLField()  # 公司网站
    description = models.CharField(max_length=1000)  # 公司描述
