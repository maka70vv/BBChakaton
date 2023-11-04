from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, FeedBackView, RegisterView, ProfileView, \
    TenderDetailView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

from . import views
from .views import TendersListView

urlpatterns = [
    path("", include(router.urls)),
    path("tags/", TagView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
    path("aside/", AsideView.as_view()),
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('tenders/<int:tender_id>/like_tender/', views.like_tender),
    path('tenders/<int:tender_id>/dislike_tender/', views.dislike_tender),
    path('tenders/', TendersListView.as_view()),
    path('tenders/<int:pk>/', TenderDetailView.as_view()),
]
