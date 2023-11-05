from rest_framework import permissions

from rest_framework import generics

from companies.models import CompanyInfo
from companies.serializers import CompanyInfoSerializer


class CompaniesListView(generics.ListAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [permissions.AllowAny]
