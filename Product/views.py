from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import date
from datetime import datetime
from django.template import loader, Context
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)
from Product.models import Ticket, TicketSale
from Company.models import Company

from Product.forms import TicketForm

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)

    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class TicketCreateView(CreateView):
    model = Ticket
    template_name = 'product/add_update/ticket_add.html'
    form_class = TicketForm
    success_url = reverse_lazy('product:tickets')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Ticket'
        return context

class TicketUpdateView(UpdateView):
    template_name = 'product/add_update/ticket_add.html'
    form_class = TicketForm
    success_url = reverse_lazy('product:tickets')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Ticket'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Ticket, slug=_slug)

class TicketListView(ListView):
    template_name = 'product/list/ticket_list.html'
    # paginate_by = 10
    queryset = Ticket.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class TicketDeleteView(DeleteView):
    template_name = 'product/delete/ticket_delete.html'
    success_url = reverse_lazy('product:tickets')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Ticket, slug=_slug)

#---------------------------End Ticket------------------------##

def ticket_sale_page(request):
    tickets = Ticket.objects.all()
    return render(request, 'product/list/tickets.html', context={'tickets': tickets})


class ProductIndexView(TemplateView):
    template_name = 'product/index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ConsultingIndexView(TemplateView):
    template_name = 'product/index_consulting.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def ticket_sale(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket_sale = TicketSale(date=timezone.now(), ticket = ticket, price = ticket.price)
    ticket_sale.save()
    template = loader.get_template('product/ticket.html')
    try:
        company = Company.objects.get(name='Theater')
    except:
        company = None
    try:
        company2 = Company.objects.get(name='Theater2')
    except:
        company2 = None
    try:
        company3 = Company.objects.get(name='Theater3')
    except:
        company3 = None
    try:
        company4 = Company.objects.get(name='Theater4')
    except:
        company4 = None
    try:
        company5 = Company.objects.get(name='Theater5')
    except:
        company5 = None
    try:
        company6 = Company.objects.get(name='Theater6')
    except:
        company6 = None
    context = {
        "ticket_sale": ticket_sale,
        "company":company,
        "company2":company2,
        "company3":company3,
        "company4":company4,
        "company5":company5,
        "company6":company6,
    }
    html = template.render(context)
    pdf = render_to_pdf('product/ticket.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" % (ticket.ref)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

class ReportingPage(View):
    template_name = 'product/reporting_page.html'

    def get(self, request):
        return render(request, "product/reporting_page.html")

def reporting(request):
    current_time = None
    if request.method == "GET":
        
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        start_date = parse_date(from_date)
        end_date = parse_date(to_date)
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = start_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        end_date = end_date.replace(hour = 23, minute = 59, second = 59, microsecond = 0)

        company = Company.objects.get(name ="Theater")
        
        ticket_sales = TicketSale.objects.filter(date__lte = end_date)
        ticket_sales = ticket_sales.filter(date__gte = start_date)

        tickets = Ticket.objects.all()

        for i in range(tickets.__len__()):
            tickets[i].calculated_sales_number = tickets[i].sales_number(start_date, end_date)
            tickets[i].calculated_sales_value = tickets[i].sales_value(start_date, end_date)
        
        total_tickets_number = total_tickets_value = 0

        total_tickets_number = ticket_sales.count()
        for i in ticket_sales:
            total_tickets_value += i.price

        template = loader.get_template('product/reporting.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "tickets": tickets,
            "total_tickets_number":total_tickets_number,
            "total_tickets_value":total_tickets_value,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('product/reporting.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "rapport de production_%s.pdf" % (timezone.now())
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")