from django.urls import path, include
from .views import CompanyCreateView
app_name = 'Company'

urlpatterns = [
    path('company-add/', CompanyCreateView.as_view(), name='company-add')
]
