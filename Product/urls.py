from django.urls import path, include
from .views import *

app_name = 'product'

urlpatterns = [
     # Main View
     path('', ProductIndexView.as_view(), name='index'),
     # Brands Url Management
     path('ticket/list/', TicketListView.as_view(), name='tickets'),
     path('ticket/create/', TicketCreateView.as_view(), name='ticket-create'),
     path('ticket/<slug>/update/', TicketUpdateView.as_view(), name='ticket-update'),
     path('ticket/<slug>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),

     path('index-consulting/', ConsultingIndexView.as_view(), name='index-consulting'),
     path('ticket-sale-page/', ticket_sale_page, name='ticket-sale-page'),
     path('ticket-sale/<slug>/', ticket_sale, name='ticket-sale'),

    path('reporting-page/', ReportingPage.as_view(), name='reporting-page'),
    path(r'^reporting/search/', reporting, name='reporting'),
    
]
