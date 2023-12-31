from django.urls import path
from . import views
from .views import TendersListView, FeedBackView, RegisterView, ProfileView, TenderDetailView, ContractsListView, ContractsDetailView

urlpatterns = [
    path("feedback/", FeedBackView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('tenders/<int:tender_id>/like_tender/', views.like_tender),
    path('tenders/<int:tender_id>/dislike_tender/', views.dislike_tender),
    path('tenders/', TendersListView.as_view()),
    path('tenders/<int:pk>/', TenderDetailView.as_view()),
    path('contracts/<int:tender_id>/like_tender/', views.like_contract),
    path('contracts/<int:tender_id>/dislike_tender/', views.dislike_contract),
    path('contracts/', ContractsListView.as_view()),
    path('contracts/<int:pk>/', ContractsDetailView.as_view()),
]
