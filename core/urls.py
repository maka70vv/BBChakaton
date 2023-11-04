from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, FeedBackView, RegisterView, ProfileView
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
    path('like_tender/<int:tender_id>/', views.like_tender, name='like_tender'),
    path('dislike_tender/<int:tender_id>/', views.dislike_tender, name='dislike_tender'),
    path('api/tenders/', TendersListView.as_view(), name='tenders_list'),
]