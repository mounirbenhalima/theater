from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)

from . forms import MachineForm, MachineTypeForm
from . models import Machine, MachineType

class MachineIndexView(TemplateView):
    template_name = 'machine/index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class MachineCreateView(CreateView):
    model = Machine
    template_name = 'machine/add_update/machine_add.html'
    form_class = MachineForm
    success_url = reverse_lazy('machine:machines')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une nouvelle machine'
        return context

class MachineTypeCreateView(CreateView):
    model = MachineType
    template_name = 'machine/add_update/machinetype_add.html'
    form_class = MachineTypeForm
    success_url = reverse_lazy('machine:machinetypes')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un nouveau type de machine'
        return context


class MachineUpdateView(UpdateView):
    template_name = 'machine/add_update/machine_add.html'
    form_class = MachineForm
    success_url = reverse_lazy('machine:machines')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour une machine'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Machine, slug=_slug)

def free_machine(request, slug):
    machine = get_object_or_404(Machine, slug=slug)
    machine.state = 'FREE'
    machine.save()
    return redirect(reverse_lazy("machine:machines"))

def empty_container(request, slug):
    container = get_object_or_404(Container, slug=slug)
    container.remaining = 0
    container.color = None
    container.mix_type = None
    container.mix_perfume = None
    container.available = "FREE"
    container.save()
    return redirect(reverse_lazy("machine:containers"))

class MachineTypeUpdateView(UpdateView):
    template_name = 'machine/add_update/machinetype_add.html'
    form_class = MachineTypeForm
    success_url = reverse_lazy('machine:machinetypes')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un type de machine'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(MachineType, slug=_slug)

class MachineListView(ListView):
    queryset = Machine.objects.all()
    template_name = 'machine/list/machine_list.html'
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class MachineTypeListView(ListView):
    queryset = MachineType.objects.all()
    template_name = 'machine/list/machinetype_list.html'
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class MachineDeleteView(DeleteView):
    template_name = 'machine/delete/machine_delete.html'
    form_class = MachineForm
    success_url = reverse_lazy('machine:machines')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Machine, slug=_slug)

class MachineTypeDeleteView(DeleteView):
    template_name = 'machine/delete/machinetype_delete.html'
    form_class = MachineTypeForm
    success_url = reverse_lazy('machine:machines')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(MachineType, slug=_slug)