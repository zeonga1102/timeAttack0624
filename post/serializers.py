from rest_framework import serializers
from .models import JobPostSkillSet, JobPost, Company


class CommpanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name']


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostSkillSet
        fields = "__all__"


class JobPostSerializer(serializers.ModelSerializer):
    company = CommpanySerializer(read_only=True)
    job_type = serializers.SerializerMethodField()
    def get_job_type(self, obj):
        return obj.job_type.job_type
    class Meta:
        model = JobPost
        fields = "__all__"
