from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company
)
from django.db.models.query_utils import Q
from .serializers import JobPostSerializer, JobPostSkillSetSerializer


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)
        job_post_list = JobPostSkillSet.objects.filter(skill_set__name__in=skills)
        jobpost_serializer = JobPostSkillSetSerializer(job_post_list, many=True).data

        return Response(jobpost_serializer, status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )
        company_name = request.data.get("company_name", None)

        jobpost_serializer = JobPostSerializer(data=request.data)

        if jobpost_serializer.is_valid():
            jobpost_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        
        return Response(jobpost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

