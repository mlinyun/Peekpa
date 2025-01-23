from django_filters import rest_framework as filters

from apps.api.serializers import JobListSerializer
from django_filters.rest_framework import DjangoFilterBackend

from apps.company.models import Company
from apps.job.models import Job, PublishJob
from rest_framework import generics, permissions
from apps.api.authentications import JWTAuthentication
from rest_framework.exceptions import ValidationError


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
