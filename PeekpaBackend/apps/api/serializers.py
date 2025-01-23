from rest_framework import serializers
from apps.company.models import Company
from apps.job.models import Resume, Job, Interview, Invitation
from apps.peekpauser.models import User, Avatar


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6, write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "token"]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email, password)
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.save()
        return user


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "first_name", "last_name", "gender", "data_join", "last_login", "is_active"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"


class AdminCompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "first_name", "last_name", "data_join"]


class AdminCompanyListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    email = serializers.CharField(write_only=True, read_only=False)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def get_user(self, obj):
        user = User.objects.filter(details__contains={"company_id": obj.id, "is_manager": True})
        if user.count():
            return AdminCompanyUserSerializer(user.all().first()).data
        return None

    class Meta:
        model = Company
        fields = ["id", "name", "website", "user", "email", "first_name", "last_name", "password"]


class JobListSerializer(serializers.ModelSerializer):
    resumes = serializers.SerializerMethodField(read_only=True)
    pass_number = serializers.SerializerMethodField()
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_tags = serializers.CharField(source="company.tags", read_only=True)
    company_avatar = serializers.CharField(source="company.avatar", read_only=True)
    company_id = serializers.CharField(source="company.id", read_only=True)

    def get_resumes(self, obj):
        return Interview.objects.filter(job__id=obj.id).count()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()

    class Meta:
        model = Job
        fields = ["id", "title", "status", "city", "location", "salary_min", "salary_max", "salary_count", "education",
                  "experience", "benefit", "publish_time", "pass_number", "hire_number", "resumes",
                  "company_name", "description",
                  "company_tags", "company_avatar", "company_id"]
        read_only_fields = ["id", "publish_time", "pass_number", "resumes", "company_name", "company_tags",
                            "company_avatar", "company_id"]


class JobSerializer(serializers.ModelSerializer):
    pass_number = serializers.SerializerMethodField()
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_tags = serializers.CharField(source="company.tags", read_only=True)
    company_size = serializers.CharField(source="company.size", read_only=True)
    company_website = serializers.CharField(source="company.website", read_only=True)
    company_id = serializers.CharField(source="company.id", read_only=True)
    resumes = serializers.SerializerMethodField()

    def get_resumes(self, obj):
        return obj.resumes.count()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()

    class Meta:
        model = Job
        fields = ["id", "title", "status", "city", "location", "salary_min", "salary_max", "salary_count", "education",
                  "pass_number", "hire_number", "experience", "benefit", "description", "publish_time", "resumes",
                  "company_name", "company_tags", "company_size", "company_website", "company_id"]
        read_only_fields = ["id", "pass_number", "publish_time", "resumes"]


class InterviewInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["id", "response", "publish_time", "due_time", "message", "update_time"]


class InterviewJobSerializer(serializers.ModelSerializer):
    pass_number = serializers.SerializerMethodField()

    def get_pass_number(self, obj):
        return Interview.objects.filter(job__id=obj.id, status=4).count()

    class Meta:
        model = Job
        fields = ["id", "pass_number", "hire_number", "title"]


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "email", "name", "gender", "details"]


class InterviewResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["name", "url"]


class InterviewSerializer(serializers.ModelSerializer):
    job = InterviewJobSerializer()
    candidate = CandidateSerializer()
    interviewer = serializers.CharField(source="interviewer.name")
    resume = InterviewResumeSerializer()
    invitation = serializers.SerializerMethodField()

    def get_invitation(self, obj):
        invitations = obj.invitations.all()
        if invitations.count():
            invitation = invitations.filter(status=obj.status)
            if invitation.count():
                return InterviewInvitationSerializer(invitation.all().first()).data
        return None

    class Meta:
        model = Interview
        fields = ["id", "job", "interviewer", "candidate", "resume", "status", "feedback", "invitation", "publish_time"]
        read_only_fields = ["resume", "candidate", "interviewer", "invitation", "publish_time"]
