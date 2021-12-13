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

from .models import Contact
from .forms import ContactForm

class ContactIndexView(TemplateView):
    template_name = 'contact/index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ContactCreateView(CreateView):
    model = Contact
    template_name = 'contact/add_update/contact_add.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contacts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Contact'
        return context

class ContactUpdateView(UpdateView):
    template_name = 'contact/add_update/contact_add.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contacts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour un Contact'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Contact, slug=_slug)

class ContactListView(ListView):
    queryset = Contact.objects.all()
    template_name = 'contact/list/contact_list.html'
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ContactDeleteView(DeleteView):
    template_name = 'contact/delete/contact_delete.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contacts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Contact, slug=_slug)