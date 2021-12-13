from django.urls import path
from . views import ContactCreateView, ContactUpdateView ,ContactIndexView, ContactListView, ContactDeleteView
app_name = 'contact'

urlpatterns = [
    #Index View
    path('', ContactIndexView.as_view(), name='index'),
    path('contact/create/', ContactCreateView.as_view(), name='add-contact'),
    path('contact/list/', ContactListView.as_view(), name='contacts'),
    path('contact/delete/<slug>/', ContactDeleteView.as_view(), name='delete-contact'),
    path('contact/update/<slug>/', ContactUpdateView.as_view(), name='update-contact'),


]