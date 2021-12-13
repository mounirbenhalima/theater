from django.shortcuts import render,reverse
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Company
from .forms import CompanyForm

class CompanyCreateView(CreateView):
    form_class = CompanyForm
    template_name = 'company/add_update/company_add.html'