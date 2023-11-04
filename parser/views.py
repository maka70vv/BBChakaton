from django.http import HttpResponse
from rest_framework.generics import ListAPIView

from parser.models import TendersList
from parser.serializers import TenderSerializer


# Create your views here.
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


class TendersListView(ListAPIView):
    queryset = TendersList.objects.all()
    serializer_class = TenderSerializer
