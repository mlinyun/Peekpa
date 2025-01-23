import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_filters import rest_framework as filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from apps.api.serializers import ResumeSerializer, AvatarSerializer, JobListSerializer, JobSerializer

from apps.job.models import Resume, Job
from apps.peekpauser.models import Avatar
from urllib.parse import unquote

from apps.api.permissions import IsGetForAll

from apps.api.authentications import PassGetAuthentication


class ResumeView(APIView):
    """简历上传视图"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        unused_resumes = Resume.objects.filter(user=self.request.user, interviews=None)
        # 删除旧的并且没有和 Interview 关联的 Resume 对象及其关联的文件
        for resume in unused_resumes:
            default_storage.delete(resume.url[6:])
            resume.delete()
        old_resumes = Resume.objects.filter(user=self.request.user)
        # 将和 Interviews 绑定的 Resume 的 is_active 设置成 False
        for resume in old_resumes:
            if resume.is_active:
                resume.is_active = False
                resume.save()
        # 获取上传文件名称
        file = request.FILES.get("resume")
        file_name = file.name
        # 拼凑存储文件名，并存储在 `/media/resume/` 目录下
        file_path = f"resume/{'.'.join(file_name.split('.')[:-1])}_{str(uuid.uuid4())[:8]}.{file_name.split('.')[-1]}"
        saved_path = default_storage.save(file_path, ContentFile(file.read()))
        resume = Resume.objects.create(name=file_name, user=self.request.user, url="media/{}".format(saved_path))
        return Response(data=ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)


class AvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        old_avatars = Avatar.objects.filter(user=self.request.user)
        # 删除旧的 Avatar 对象及其关联的文件
        for avatar in old_avatars:
            default_storage.delete(avatar.url[6:])
        old_avatars.delete()
        # 获取上传文件名称
        file = request.FILES.get("avatar")
        file_name = file.name
        # 拼凑存储文件名，并存储在 `/media/avatar/` 目录下
        file_path = f"avatar/{'.'.join(file_name.split('.')[:-1])}_{str(uuid.uuid4())[:8]}.{file_name.split('.')[-1]}"
        saved_path = default_storage.save(file_path, ContentFile(file.read()))
        avatar = Avatar.objects.create(name=file_name, user=self.request.user, url="media/{}".format(saved_path))
        return Response(data=AvatarSerializer(avatar).data, status=status.HTTP_201_CREATED)


class JobListFilter(filters.FilterSet):
    q = filters.CharFilter(method="my_custom_filter", label="Search")
    order = filters.CharFilter(method="order_search", label="Order")
    experience = filters.CharFilter(method="experience_search", label="Experience")
    education = filters.CharFilter(method="education_search", label="Education")

    class Meta:
        model = Job
        fields = ["q", "order", "education", "experience"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__contains=value) | Q(city__contains=value) | Q(location__contains=value) | Q(
                company__name__contains=value)
        )

    def education_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(education=decoded_data)
        return queryset

    def experience_search(self, queryset, name, value):
        decoded_data = unquote(value)
        if value:
            return queryset.filter(experience=decoded_data)
        return queryset

    def order_search(self, queryset, name, value):
        if value == "newest":
            return queryset.order_by("-publish_time")
        return queryset


class JobListView(generics.ListAPIView):
    queryset = Job.objects.filter(status=Job.STATUS_PUBLISH).order_by("title")
    serializer_class = JobListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobListFilter


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(status=Job.STATUS_PUBLISH)
    serializer_class = JobSerializer
    authentication_classes = [PassGetAuthentication]
    permission_classes = [IsGetForAll]
    lookup_field = "id"
