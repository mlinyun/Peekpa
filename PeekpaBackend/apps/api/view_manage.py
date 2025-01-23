from django_filters import rest_framework as filters

from apps.api.serializers import JobListSerializer, JobSerializer, InterviewSerializer
from django_filters.rest_framework import DjangoFilterBackend

from apps.company.models import Company
from apps.job.models import Job, PublishJob, Interview
from rest_framework import generics, permissions, status
from apps.api.authentications import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class JobListFilter(filters.FilterSet):
    q = filters.CharFilter(method="my_custom_filter", label="Search")

    class Meta:
        model = Job
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(title__contains=value)


class ManageJobListView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobListFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_manager = self.request.user.details.get("is_manager", False)
        company_id = self.request.user.details.get("company_id", -1)
        queryset = queryset.filter(company__id=company_id)
        if not is_manager:
            job_ids = PublishJob.objects.filter(user__uid=self.request.user.uid).values_list("job_id", flat=True)
            queryset = queryset.filter(id__in=job_ids)
        return queryset

    def perform_create(self, serializer):
        company = self.request.user.details.get("company_id")
        if company:
            job = serializer.save()
            company_obj = Company.objects.get(id=company)
            company_obj.jobs.add(job)
            publish_job_obj = PublishJob(user=self.request.user, job=job)
            publish_job_obj.save()
        else:
            raise ValidationError


class ManageJobNameListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        is_manager = self.request.user.details.get("is_manager", False)
        company = self.request.user.details.get("company_id")
        job_list = Job.objects.filter(company__id=company)
        if not is_manager:
            jobs = PublishJob.objects.filter(user__uid=self.request.user.uid)
            job_list = [item.job for item in jobs]
        content = []
        for item in job_list:
            content.append({
                "id": item.id,
                "title": item.title,
            })
        return Response(data=content, status=status.HTTP_200_OK)


class ManageJobDetailView(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.user.details.get("company_id", -1)
        queryset = queryset.filter(company__id=company_id)
        return queryset

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class ManageInterviewListView(generics.ListAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        job_id = self.kwargs["id"]
        is_manager = self.request.user.details.get("is_manager", False)
        company_id = self.request.user.details.get("company_id", -1)
        if job_id == "all":
            # 获取全部的面试信息
            jobs_id = PublishJob.objects.filter(user__details__contains={"company_id": company_id}).values_list(
                "job_id", flat=True)
            queryset = queryset.filter(job__id__in=jobs_id)
        else:
            # 获取当前职位的面试信息
            queryset = queryset.filter(job__id=job_id)
        # 获取当前公司职员所管理的面试信息
        if not is_manager:
            queryset = queryset.filter(interviewer__uid=self.request.user.uid)
        return queryset


class ManageInterviewDetailView(generics.RetrieveUpdateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

    def get_object(self):
        job_id = self.kwargs["id"]
        interview_id = self.kwargs["iid"]
        queryset = self.get_queryset()
        is_manager = self.request.user.details.get("is_manager", False)
        company_id = self.request.user.details.get("company_id", -1)
        jobs_id = PublishJob.objects.filter(user__details__contains={"company_id": company_id}).values_list(
            "job_id", flat=True)
        if is_manager:
            obj = get_object_or_404(queryset, job__id__in=jobs_id, job__id=job_id, id=interview_id)
        else:
            obj = get_object_or_404(queryset, job__id__in=jobs_id, job__id=job_id, id=interview_id,
                                    interview__uid=self.request.user.uid)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def patch(self, request, *args, **kwargs):
        interview = self.get_object()
        serializer = self.get_serializer(interview, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data.get("status", 0) == 4:
            pass_number = Interview.objects.filter(job__id=interview.job.id, status=8).count()
            pass_number += 1
            if pass_number == interview.job.hire_number:
                interview.job.status = 2
            interview.job.save()
        return Response(data=serializer.data)
