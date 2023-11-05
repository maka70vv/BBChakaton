from django.urls import path
from .views import CompaniesListView

urlpatterns = [
    path("rating/", CompaniesListView.as_view())
]
