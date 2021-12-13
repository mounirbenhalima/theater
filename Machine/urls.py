from django.urls import path
from . views import *
app_name = 'machine'

urlpatterns = [
    #Index View
    path('', MachineIndexView.as_view(), name='index'),
    # Machine Creation Url
    path('machine/create/machine/', MachineCreateView.as_view(), name='machine-create'),
    path('machine/create/machine-type/', MachineTypeCreateView.as_view(), name='machinetype-create'),
    # Machine Update Url
    path('machine/machine/<slug>/update/', MachineUpdateView.as_view(), name='machine-update'),
    path('machine/machine/<slug>/free/', free_machine, name='machine-free'),
    path('machine/mahcinetype/<slug>/update', MachineTypeUpdateView.as_view(), name='machinetype-update'),
    # Machine List Url
    path('machine/list/machine/', MachineListView.as_view(), name='machines'),
    path('machine/list/machine-type/', MachineTypeListView.as_view(), name='machinetypes'),
    # Machine Delete Url
    path('machine/machine/<slug>/delete/',MachineDeleteView.as_view(), name='machine-delete'),
    path('machine/machinetype/<slug>/delete/',MachineTypeDeleteView.as_view(), name='machinetype-delete'),

]