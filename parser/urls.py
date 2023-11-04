# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('posts', PostViewSet, basename='posts')

from . import views
from .views import TendersListView

urlpatterns = [
    # path("", include(router.urls)),
    path('like_tender/<int:tender_id>/', views.like_tender, name='like_tender'),
    path('dislike_tender/<int:tender_id>/', views.dislike_tender, name='dislike_tender'),
    path('api/tenders/', TendersListView.as_view(), name='tenders_list'),
]
