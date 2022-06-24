from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company,
)
from .serializers import JobPostSerializer


class SkillView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        
        job_skills = JobPostSkillSet.objects.filter(skill_set__name__in=skills)
        job_post = JobPost.objects.filter(id__in=[ js.job_post.id for js in job_skills ])
        jobpost_serializer = JobPostSerializer(job_post, many=True).data

        return Response(jobpost_serializer, status=status.HTTP_200_OK)


class JobView(APIView):

    def post(self, request):
        job_type = int( request.data.get("job_type", None) )

        job_type_qs = JobType.objects.filter(id=job_type)
        if not job_type_qs.exists():
            return Response({"message": "invalid job type"}, status=status.HTTP_400_BAD_REQUEST)

        company_name = request.data.get("company_name", None)
        company = Company.objects.filter(company_name=company_name)

        if not company.exists():
            company = Company(company_name=company_name)
            company.save()
        else:
            company = company.first()

        jobpost_serializer = JobPostSerializer(data=request.data)

        if jobpost_serializer.is_valid():
            jobpost_serializer.save(company=company, job_type=job_type_qs.first())
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        
        return Response(jobpost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
