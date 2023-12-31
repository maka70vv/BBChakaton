from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView

from .serializers import ContactSerailizer, RegisterSerializer, UserSerializer, \
    TenderSerializer, ContractSerializer
from .models import TendersList, ContractsList
from rest_framework.response import Response
from rest_framework import pagination
from rest_framework import generics


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args,  **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


def like_tender(request, tender_id):
    tender = TendersList.objects.get(pk=tender_id)
    tender.likes += 1
    tender.save()
    return HttpResponse(status=200)


def dislike_tender(request, tender_id):
    tender = TendersList.objects.get(pk=tender_id)
    tender.dislikes += 1
    tender.save()
    return HttpResponse(status=200)


def like_contract(request, tender_id):
    contract = ContractsList.objects.get(pk=tender_id)
    contract.likes += 1
    contract.save()
    return HttpResponse(status=200)


def dislike_contract(request, tender_id):
    contract = ContractsList.objects.get(pk=tender_id)
    contract.dislikes += 1
    contract.save()
    return HttpResponse(status=200)


class TendersListView(generics.ListAPIView):
    queryset = TendersList.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class ContractsListView(generics.ListAPIView):
    queryset = ContractsList.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination



class TenderDetailView(generics.RetrieveAPIView):
    queryset = TendersList.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.AllowAny]


class ContractsDetailView(generics.RetrieveAPIView):
    queryset = TendersList.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['25.makarovv@gmail.com'])
            return Response({"success": "Sent"})
