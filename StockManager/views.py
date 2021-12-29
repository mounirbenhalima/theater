from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.forms import inlineformset_factory, forms
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import date
from datetime import datetime
from django.urls import reverse_lazy, resolve
from django.core.mail import send_mail, EmailMessage
from .forms import ContactChoiceForm, TrashOutForm, CoilEntryForm, SparePartConsumptionForm, CoilSaleForm
from django.db import IntegrityError
from django.utils.crypto import get_random_string
import io
from django.db.models import Q
from django.http import FileResponse
from reportlab.pdfgen import canvas
from decimal import Decimal
from .utils import render_to_pdf

from .controllers import order_redirect

from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)

from Product.models import Product, Color, Coil, RawMatter, FinishedProduct, FinishedProductType, CoilType, Trash, Handle, Labelling, Package, Tape, SparePart
from Company.models import Company
from .models import Order, OrderItem, TrashOut, Loss, OrderHandle, OrderLabelling, OrderPackage, OrderTape, OrderSparePart, SparePartConsumption, CoilSale
from Machine.models import Machine
from Production.forms import GeneralTrashForm
from Production.models import Production, Correction, TrashCorrection, GapRawMatter, GapHandle, GapLabelling, GapPackage, HandleConsumption, LabellingConsumption, PackageConsumption
from django.template import loader, Context

class HandleIndexView(View):
    template_name = 'stock_manager/index_handle.html'

    def get(self, request):
        return render(request, "stock_manager/index_handle.html")

class LabellingIndexView(View):
    template_name = 'stock_manager/index_labelling.html'

    def get(self, request):
        return render(request, "stock_manager/index_labelling.html")

class PackageIndexView(View):
    template_name = 'stock_manager/index_package.html'

    def get(self, request):
        return render(request, "stock_manager/index_package.html")

class TapeIndexView(View):
    template_name = 'stock_manager/index_tape.html'

    def get(self, request):
        return render(request, "stock_manager/index_tape.html")


class RawMatterIndexView(View):
    template_name = 'stock_manager/index_rawmatter.html'

    def get(self, request):
        return render(request, "stock_manager/index_rawmatter.html")

class FinishedProductIndexView(View):
    template_name = 'stock_manager/index_finalproduct.html'

    def get(self, request):
        return render(request, "stock_manager/index_finalproduct.html")

class ConsumablesIndexView(View):
    template_name = 'stock_manager/index_consumables.html'

    def get(self, request):
        return render(request, "stock_manager/index_consumables.html")

class SparePartIndexView(View):
    template_name = 'stock_manager/index_spare_part.html'

    def get(self, request):
        return render(request, "stock_manager/index_spare_part.html")

class CoilsIndexView(View):
    template_name = 'stock_manager/index_coil.html'

    def get(self, request):
        return render(request, "stock_manager/index_coil.html")

class ControlIndexView(View):
    template_name = 'stock_manager/index_control.html'

    def get(self, request):
        return render(request, "stock_manager/index_control.html")

class TrashIndexView(View):
    template_name = 'stock_manager/index_trash.html'

    def get(self, request):
        return render(request, "stock_manager/index_trash.html")


class IndexView(View):
    template_name = 'stock_manager/index.html'

    def get(self, request):
        return render(request, "stock_manager/index.html")

# ----------------Handle-----------------


@login_required(login_url=reverse_lazy('login'))
def handle_entry(request):
    context = {
        'product_list': Handle.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Cordon'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

@login_required(login_url=reverse_lazy('login'))
def handle_out(request):
    context = {
        'product_list': Handle.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Cordon'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

# ----------------Labelling-----------------


@login_required(login_url=reverse_lazy('login'))
def labelling_entry(request):
    context = {
        'product_list': Labelling.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Labelling'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

@login_required(login_url=reverse_lazy('login'))
def labelling_out(request):
    context = {
        'product_list': Labelling.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Labelling'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

# ----------------Packaging-----------------


@login_required(login_url=reverse_lazy('login'))
def package_entry(request):
    context = {
        'product_list': Package.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Emballage'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

@login_required(login_url=reverse_lazy('login'))
def package_out(request):
    context = {
        'product_list': Package.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Emballage'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

# ----------------Tape-----------------


@login_required(login_url=reverse_lazy('login'))
def tape_entry(request):
    context = {
        'product_list': Tape.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Scotch'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

@login_required(login_url=reverse_lazy('login'))
def tape_out(request):
    context = {
        'product_list': Tape.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Scotch'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


# ----------------Spare Part-----------------


@login_required(login_url=reverse_lazy('login'))
def part_entry(request):
    context = {
        'product_list': SparePart.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Pièce de Rechange'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

@login_required(login_url=reverse_lazy('login'))
def part_out(request):
    context = {
        'product_list': SparePart.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Pièce de Rechange'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


class SparePartConsumptionView(View):
    model = SparePartConsumption
    template_name = 'stock_manager/part_consumption.html'
    success_url = reverse_lazy('stock-manager:part-consumption')

    def get(self, request, *arg, **kwargs):
        form = SparePartConsumptionForm()
        context = {
            'form': form,
        }
        return render(self.request, 'stock_manager/part_consumption.html', context)

    def post(self, request, *args, **kwargs):
        form = SparePartConsumptionForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                part = form.part

                if part != None:
                    quantity = form.quantity
                    mchn = form.machine
                    intervention_type = form.intervention_type
                    machine = Machine.objects.get(slug=mchn.slug)
                    user = request.user
                    part_consumption = SparePartConsumption(date=timezone.now(), quantity = quantity, user=user, part = part, intervention_type = intervention_type , machine=machine)
                    if quantity <= part.quantity:
                        part.quantity = part.quantity - quantity
                    else:
                        messages.error(
                        request, "Pièce Non Disponible En Stock")
                        return redirect(request.META.get('HTTP_REFERER'))
                    part.save()
                    part_consumption.save()
                    return redirect(self.success_url)
                else:
                    messages.error(
                        request, "Pièce Inexistante")
                    return redirect(reverse_lazy("stock-manager:part-consumption"))
# ----------------RAW MATTER-----------------


@login_required(login_url=reverse_lazy('login'))
def raw_matter_entry(request):
    context = {
        'product_list': RawMatter.objects.all(),
        "STOCK_TYPE": "STOCK_ENTRY",
        "form_name": "Entrée de stock 'Matière Première'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_ENTRY' and active_order[0].items.last().item.slug.split('-')[0] == 'rawmatter':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


@login_required(login_url=reverse_lazy('login'))
def raw_matter_out(request):
    if request.user.profile.job_position.name == "Gestionnaire de Stock":
        context = {
        'product_list': RawMatter.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Matière Première'"
        }
    elif request.user.profile.job_position.name == "Mélangeur":
        context = {
            'product_list': RawMatter.objects.exclude(name__name="encre").all(),
            "STOCK_TYPE": "STOCK_OUT",
            "form_name": "Sortie de stock 'Matière Première'"
        }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT' and active_order[0].items.last().item.slug.split('-')[0] == 'rawmatter':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


@login_required(login_url=reverse_lazy('login'))
def raw_matter_return(request):
    context = {
        'product_list': RawMatter.objects.all(),
        "STOCK_TYPE": "STOCK_RETURN",
        "form_name": "Retour de stock 'MATIERE PREMIERE'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_RETURN' and active_order[0].items.last().item.slug.split('-')[0] == 'rawmatter':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)

# ----------------FINAL PRODUCT-----------------

def delete_final_product(request, slug):
    production = get_object_or_404(Production, slug=slug)
    production.delete()
    return redirect(reverse_lazy("stock-manager:final-product-entry"))


@login_required(login_url=reverse_lazy('login'))
def final_product_entry(request):
    if request.method == "POST":
        difference = 0
        qte = 0
        quantity = int(request.POST.get("quantity"))
        production_slug = request.POST.get("get_production")
        production = get_object_or_404(Production, slug = production_slug)
        if production.state == "PENDING":
            production.state = "FINISHED"
            production.save()
            product = production.product
            difference = quantity - production.quantity_produced
            production.quantity_produced = quantity
            production.save()
            finalproduct = FinishedProductType.objects.get(product_designation= product.product_designation)
            qte = finalproduct.quantity + quantity
            try:
                package = Package.objects.get(slug=finalproduct.package.slug)
                package.quantity_workshop = package.quantity_workshop - quantity
                package_consumption = PackageConsumption(user = production.user, date = timezone.now(), package = package, machine = production.machine, quantity = quantity)
                package_consumption.save()
                package.save()
            except:
                pass
            
            finalproduct.quantity = qte
            finalproduct.save()
                
            if difference < 0:
                correction = Correction(date = timezone.now(), user = request.user, production = production, difference = difference, type_difference = "NEGATIVE")
                correction.save()
            elif difference > 0:
                correction = Correction(date = timezone.now(), user = request.user, production = production, difference = difference, type_difference = "POSITIVE")
                correction.save()
        else:
            messages.error(request, "Production Déjà Validée")
            return render(request,'stock_manager/list/production.html',context={'object_list':Production.objects.filter(state="PENDING", process_type="FINISHED_PRODUCT")})
    return render(request,'stock_manager/list/production.html',context={'object_list':Production.objects.filter(state="PENDING", process_type="FINISHED_PRODUCT")})



class FinishedProductListView(ListView):

    template_name = 'stock_manager/list/production.html'

    def get_queryset(self,**kwargs):
        queryset = Production.objects.filter(state="PENDING", process_type="FINISHED_PRODUCT")
        return queryset

@login_required(login_url=reverse_lazy('login'))
def final_product_out(request):
    context = {
        'product_list': FinishedProductType.objects.all(),
        "STOCK_TYPE": "STOCK_OUT",
        "form_name": "Sortie de stock 'Produit Fini'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_OUT' and active_order[0].items.last().item.slug.split('-')[0] == 'finishedproducttype':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


@login_required(login_url=reverse_lazy('login'))
def final_product_return(request):
    context = {
        'product_list': FinishedProductType.objects.all(),
        "STOCK_TYPE": "STOCK_RETURN",
        "form_name": "Retour de stock 'Produit Fini'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_RETURN' and active_order[0].items.last().item.slug.split('-')[0] == 'finishedproducttype':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)
# ----------------COIL-----------------
class CoilEntryView(View):
    model = Coil
    template_name = 'stock_manager/coil_entry.html' 
    success_url = reverse_lazy('stock-manager:entry-coil-list')
    
    def get(self, request, *arg, **kwargs):
        form = CoilEntryForm()
        context= {
        'form':form,
        }
        return render(self.request, 'stock_manager/coil_entry.html', context)

    def post(self, request, *args, **kwargs):
        form = CoilEntryForm(request.POST)
        
        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                product = form.type_coil
                source = form.supplier
                user = request.user
                ref = get_random_string(15)
                coil = Coil(introducer = user, type_coil = product, ref =ref, creation_date = timezone.now() , name = product.name, quantity = 1, status ="PENDING_DATA" , type_name = product.type_name, capacity = product.capacity, perfume = product.perfume, link = product.link, brand = product.brand, color = product.color, supplier = source, warehouse = product.warehouse)
                coil.save()
                return redirect (self.success_url)

def entry_coil_list(request):
    weight = None
    micronnage = None
    coil = None
    if request.method == "POST":
        weight = Decimal(request.POST.get("weight"))
        micronnage = Decimal(request.POST.get("micronnage"))
        coil_slug = request.POST.get("get_coil")
        coil = get_object_or_404(Coil, slug = coil_slug)
        coil.weight = weight
        coil.micronnage = micronnage
        coil.status = "IN_STOCK"
        coil.ticket_printed = True
        coil.save()
    return render(request,'stock_manager/entry_coil_list.html',context={'object_list':Coil.objects.filter(user = None )})

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Créer Bobine'
        return context

class QuarantineCoilListView(ListView):

    template_name = 'stock_manager/quarantine_coil.html'

    def get_queryset(self, **kwargs):
        queryset = Coil.objects.filter(status="TO_BE_DESTROYED", destroyed= False)
        return queryset


class CoilsListView(ListView):

    template_name = 'stock_manager/list/coils.html'

    def get_queryset(self,**kwargs):
        queryset = Coil.objects.filter(status="IN_STOCK") | Coil.objects.filter(status="QUARANTINE") | Coil.objects.filter(status="TO_BE_DESTROYED", destroyed=False)
        return queryset
    
@login_required(login_url=reverse_lazy('login'))
def coil_return(request):
    context = {
        'product_list': CoilType.objects.all(),
        "STOCK_TYPE": "STOCK_RETURN",
        "form_name": "Retour de stock 'BOBINE'"
    }
    active_order = Order.objects.filter(user=request.user, ordered=False)
    if active_order:
        if active_order[0].type_order == 'STOCK_RETURN' and active_order[0].items.last().item.slug.split('-')[0] == 'coiltype':
            return render(request, "stock_manager/stock_list.html", context)
        else:
            return redirect(reverse_lazy("stock-manager:order-summary"))
    else:
        return render(request, "stock_manager/stock_list.html", context)


def destroy_coil(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    coil.destroyed = True
    coil.save()
    return redirect(reverse_lazy("stock-manager:quarantine-coil"))


class CoilSale(View):
    model = CoilSale
    template_name = 'stock_manager/coil_sale.html'
    success_url = reverse_lazy('stock-manager:coil-sale')

    def get(self, request, *arg, **kwargs):
        form = CoilSaleForm()
        context = {
            'form': form,
        }
        return render(self.request, 'stock_manager/coil_sale.html', context)

    def post(self, request, *args, **kwargs):
        form = CoilSaleForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                coil = None
                form = form.save(commit=False)
                product = request.POST.get('_ref')
                try:
                    coil = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product)
                except Coil.DoesNotExist:
                    coil = None
                if coil != None:
                    client = form.client
                    user = request.user
                    coil.sale_date = timezone.now()
                    coil.client = client
                    coil.status = "SOLD"
                    coil.save()
                    messages.success(
                        request, "Opération Effectuée")
                    return redirect(self.success_url)
                else:
                    messages.error(
                        request, "Référence Inexistante")
                    return redirect(reverse_lazy("stock-manager:coil-sale"))
###################################################################


def add_to_cart(request, slug):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = None
    try:
        try:
            try:
                try:
                    try:
                        item = get_object_or_404(Product, slug=slug)
                        if order is not None:
                            for i in order.items.all():
                                if i.item.slug == item.slug:
                                    order.items.remove(i)
                                    orderitem = OrderItem.objects.get(identifier=i.identifier)
                                    orderitem.delete()
                        identifier = get_random_string(10)
                        order_item, created = OrderItem.objects.get_or_create(
                        item=item,
                        user=request.user,
                        ordered=False,
                        identifier = identifier
                        )
                    except:
                        item = get_object_or_404(Handle, slug=slug)
                        if order is not None:
                            for i in order.tapes.all():
                                if i.item.slug == item.slug:
                                    order.handles.remove(i)
                                    orderitem = OrderHandle.objects.get(identifier=i.identifier)
                                    orderitem.delete()
                        identifier = get_random_string(10)
                        order_item, created = OrderHandle.objects.get_or_create(
                        item=item,
                        user=request.user,
                        ordered=False,
                        identifier = identifier
                        )
                except:
                    item = get_object_or_404(Tape, slug=slug)
                    if order is not None:
                        for i in order.tapes.all():
                            if i.item.slug == item.slug:
                                order.tapes.remove(i)
                                orderitem = OrderTape.objects.get(identifier=i.identifier)
                                orderitem.delete()
                    identifier = get_random_string(10)
                    order_item, created = OrderTape.objects.get_or_create(
                    item=item,
                    user=request.user,
                    ordered=False,
                    identifier = identifier
                    )
            except:
                item = get_object_or_404(Package, slug=slug)
                if order is not None:
                    for i in order.packages.all():
                        if i.item.slug == item.slug:
                            order.packages.remove(i)
                            orderitem = OrderPackage.objects.get(identifier=i.identifier)
                            orderitem.delete()
                identifier = get_random_string(10)
                order_item, created = OrderPackage.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False,
                identifier = identifier
                )
        except:
            item = get_object_or_404(Labelling, slug=slug)
            if order is not None:
                for i in order.labellings.all():
                    if i.item.slug == item.slug:
                        order.labellings.remove(i)
                        orderitem = OrderLabelling.objects.get(identifier=i.identifier)
                        orderitem.delete()
            identifier = get_random_string(10)
            order_item, created = OrderLabelling.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
            identifier = identifier
            )
    except:
        item = get_object_or_404(SparePart, slug=slug)
        if order is not None:
            for i in order.parts.all():
                if i.item.slug == item.slug:
                    order.parts.remove(i)
                    orderitem = OrderSparePart.objects.get(identifier=i.identifier)
                    orderitem.delete()
        identifier = get_random_string(10)
        item = get_object_or_404(SparePart, slug=slug)
        order_item, created = OrderSparePart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        identifier = identifier
        )


    redirect_value = slug.split("-")[0]
    if redirect_value =="handle":
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Enter Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
    
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.handles.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                order.category = "Cordon"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
            else:
                order.handles.add(order_item)
                order_item.quantity = int(tmp_quantity)
                order.category = "Cordon"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=ordered_date,
                type_order=STOCK_TYPE)
    
            # Add Item to Order
            order.handles.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            order.category = "Cordon"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

    elif redirect_value =="labelling":
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Enter Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
    
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.labellings.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                order.category = "Labelling"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
            else:
                order.labellings.add(order_item)
                order_item.quantity = int(tmp_quantity)
                order.category = "Labelling"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=ordered_date,
                type_order=STOCK_TYPE)
    
            # Add Item to Order
            order.labellings.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            order.category = "Labelling"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

    elif redirect_value =="package":
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Enter Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
    
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.packages.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                order.category = "Emballage"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
            else:
                order.packages.add(order_item)
                order_item.quantity = int(tmp_quantity)
                order.category = "Emballage"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=ordered_date,
                type_order=STOCK_TYPE)
    
            # Add Item to Order
            order.packages.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            order.category = "Emballage"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

    elif redirect_value =="tape":
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Enter Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
    
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.tapes.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                order.category = "Scotch"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
            else:
                order.tapes.add(order_item)
                order_item.quantity = int(tmp_quantity)
                order.category = "Scotch"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=ordered_date,
                type_order=STOCK_TYPE)
    
            # Add Item to Order
            order.tapes.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            order.category = "Scotch"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

    elif redirect_value =="part":
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Enter Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()
    
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.parts.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                order.category = "Pièce de Rechange"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
            else:
                order.parts.add(order_item)
                order_item.quantity = int(tmp_quantity)
                order.category = "Pièce de Rechange"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)
    
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user,
                ordered_date=ordered_date,
                type_order=STOCK_TYPE)
    
            # Add Item to Order
            order.parts.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            order.category = "Pièce de Rechange"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

    else :
        tmp_quantity = 0
        STOCK_TYPE = ''
        if request.method == "POST":
            tmp_quantity = request.POST.get(f'{item.id}')
            STOCK_TYPE = request.POST.get('stock_value')
            if tmp_quantity == None or tmp_quantity == "":
                messages.error(request, "Entrez Une Valeur")
            else:
                order_item.quantity = int(tmp_quantity)
                order_item.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity = int(tmp_quantity)
                tmp_cat = order.items.last().item.slug.split("-")[0]
                if tmp_cat =="rawmatter":
                    order.category = "Matière Première"
                elif tmp_cat =="finishedproducttype":
                    order.category = "Produit Fini"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

            else:
                order.items.add(order_item)
                order_item.quantity = int(tmp_quantity)
                tmp_cat = order.items.last().item.slug.split("-")[0]
                if tmp_cat =="rawmatter":
                    order.category = "Matière Première"
                elif tmp_cat =="finishedproducttype":
                    order.category = "Produit Fini"
                order_item.save()
                return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)

        else:
            ordered_date = timezone.now()
            if request.user.profile.job_position.name == "Gestionnaire de Stock":
                order = Order.objects.create(
                    user=request.user,
                    ordered_date=ordered_date,
                    type_order=STOCK_TYPE)
            elif request.user.profile.job_position.name == "Mélangeur":
                order = Order.objects.create(
                    user=request.user,
                    ordered_date=ordered_date,
                    type_order=STOCK_TYPE)

            # Add Item to Order
            order.items.add(order_item)
            order_item.quantity = int(tmp_quantity)
            # Choose the Order Category
            tmp_cat = order.items.last().item.slug.split("-")[0]
            if tmp_cat =="rawmatter":
                order.category = "Matière Première"
            elif tmp_cat =="finishedproducttype":
                order.category = "Produit Fini"
            order.save()
            order_item.save()
            return order_redirect(redirect_value, order.type_order, order_qs[0].user, request.user)


class EntryStockList(ListView):
    template_name = 'stock_manager/list/entry_orders.html'
    queryset = Order.objects.filter(ordered=True)


class OrderSummaryView(LoginRequiredMixin, View):
    template_name = 'stock_manager/list/order_summary.html'
    form = ContactChoiceForm()

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
                messages.error(
                    self.request, "Vous N'Avez Aucune Commande Active".upper())
                return redirect(self.request.META.get('HTTP_REFERER'))
        if order.category == "Cordon":
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.handles.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)
        elif order.category == "Labelling":
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.labellings.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)

        elif order.category == "Emballage":
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.packages.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)

        elif order.category == "Scotch":
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.tapes.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)

        elif order.category == "Pièce de Rechange":
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.parts.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)

        else :
            context = {
                'object': order,
                'form': self.form,
                'order_product' : order.items.first().item.slug.split('-')[0]
            }
            return render(self.request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = ContactChoiceForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            try:
                if request.user.profile.job_position.name == "Gestionnaire de Stock":
                    order = Order.objects.get(user=self.request.user, ordered=False)
                    order.supplier = form.supplier
                    order.client = form.client
                    internal_stock = request.POST.get('_internal_stock')
                    external_stock = request.POST.get('_external_stock')
                    if internal_stock == "on":
                        order.external_stock = False
                    elif external_stock == "on":
                        order.external_stock = True
                    else:
                        order.external_stock = False
                        
                    order.intern_user = form.intern_user
                    order.company = form.company
                    order.type_consumption = form.type_consumption
                    if order.type_consumption == None or order.type_consumption == "":
                        order.type_consumption = "EXTERNAL"
                    order.save()

                elif request.user.profile.job_position.name == "Mélangeur":
                    order = Order.objects.get(user=self.request.user, ordered=False, machine = None)
                    order.machine = form.machine
                    order.type_consumption = form.type_consumption
                    if order.type_consumption == None or order.type_consumption == "":
                        order.type_consumption = "EXTERNAL"
                    order.save()

                return redirect('stock-manager:order-summary')

                
            except:
                pass
            return redirect('stock-manager:order-summary')


def delete_order(request, slug):
    order = get_object_or_404(Order, slug = slug)
    
    if order.user.profile.job_position.name == "Mélangeur":

        for item in order.items.all():
            item.item.quantity_workshop += item.quantity

            item.item.save()

        order.delete()

        if request.user.profile.job_position.name == "Mélangeur":
            return redirect(reverse_lazy("production:mixing-list"))
        else:
            return redirect(reverse_lazy("production:mixing-consulting"))

    elif order.user.profile.job_position.name == "Gestionnaire de Stock":
        if order.type_order == "STOCK_OUT":
            if order.intern_user is not None:
                for item in order.items.all():
                    item.item.quantity += item.quantity
                    item.item.quantity_workshop -= item.quantity * item.item.weight
                    item.item.save()
            else:
                if order.external_stock is False:
                    for item in order.items.all():
                        item.item.quantity += item.quantity
                        item.item.save()
                elif order.external_stock is True:
                    for item in order.items.all():
                        item.item.external_quantity += item.quantity
                        item.item.save()
        elif order.type_order == "STOCK_ENTRY" or order.type_order == "STOCK_RETURN":
            for item in order.items.all():
                item.item.quantity -= item.quantity
                item.item.save()
        
        order.delete()

        return redirect(reverse_lazy("production:order-consulting"))


def validate_order(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        if order.category == "Cordon":
            for order_item in order.handles.all():
                item = get_object_or_404(Handle, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        item.quantity -= order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                try:
                    item.ordered = True
                    item.save()
                except IntegrityError:
                        error_message = f"* Quantité du produit '{item}' est supérieure à celle du Stock   "
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            
            return redirect(order.get_absolute_url())

        elif order.category == "Labelling":
            for order_item in order.labellings.all():
                item = get_object_or_404(Labelling, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        item.quantity -= order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    # if order.user.profile.job_position.name == 'Mélangeur':                    
                    #     item.quantity_workshop -= order_item.quantity
                try:
                    item.save()
                except IntegrityError:
                        error_message = f"* Quantité de '{item}' est supérieure à celle du Stock   "
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            
            return redirect(order.get_absolute_url())

        elif order.category == "Emballage":
            for order_item in order.packages.all():
                item = get_object_or_404(Package, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        item.quantity -= order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    # if order.user.profile.job_position.name == 'Mélangeur':                    
                    #     item.quantity_workshop -= order_item.quantity
                try:
                    item.save()
                except IntegrityError:
                        error_message = f"* Quantité de '{item}' est supérieure à celle du Stock   "
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            
            return redirect(order.get_absolute_url())

        elif order.category == "Scotch":
            for order_item in order.tapes.all():
                item = get_object_or_404(Tape, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        item.quantity -= order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    # if order.user.profile.job_position.name == 'Mélangeur':                    
                    #     item.quantity_workshop -= order_item.quantity
                try:
                    item.save()
                except IntegrityError:
                        error_message = f"Quantité de '{item}' est supérieure à celle du Stock"
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            
            return redirect(order.get_absolute_url())

        elif order.category == "Pièce de Rechange":
            for order_item in order.parts.all():
                item = get_object_or_404(SparePart, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        item.quantity -= order_item.quantity
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    # if order.user.profile.job_position.name == 'Mélangeur':                    
                    #     item.quantity_workshop -= order_item.quantity
                try:
                    item.save()
                except IntegrityError:
                        error_message = f"Quantité de '{item}' est supérieure à celle du Stock"
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            
            return redirect(order.get_absolute_url())
            
        else:
            for order_item in order.items.all():
                item = get_object_or_404(Product, slug=order_item.item.slug)
                if order.type_order == "STOCK_ENTRY":
                    item.quantity += order_item.quantity
                if order.type_order == "STOCK_RETURN":
                    if order.client.last_name == "NL" and order.client.first_name == "Pharma (Dépôt)":
                        item.external_quantity -= order_item.quantity
                        item.quantity += order_item.quantity
                    else:
                        item.quantity += order_item.quantity
                if order.type_order == "STOCK_OUT":
                    if order.type_consumption == 'INTERNAL':
                        item.quantity -= order_item.quantity
                        item.quantity_workshop += order_item.quantity * item.weight
                        # if item.quantity < item.threshold:
                        #     try:
                        #         email(request, 'Seuil Minimal Atteint', f'Bonjour,\n Vous avez atteint le seuil minimal de "{item.product_designation}"\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
                        #     except:
                        #         pass
                    elif order.type_consumption == 'EXTERNAL':
                        if order.user.profile.job_position.name == 'Gestionnaire de Stock':
                            if order.category == "Produit Fini":
                                if order.client.last_name == "NL" and order.client.first_name == "Pharma (Dépôt)":
                                    item.quantity -= order_item.quantity
                                    item.external_quantity += order_item.quantity
                                else:
                                    if order.external_stock is True:
                                        item.external_quantity -= order_item.quantity
                                    else:
                                        item.quantity -= order_item.quantity
                                # if item.quantity < item.threshold:
                                #     try:
                                #         email(request, "Seuil Minimal Atteint", f'Bonjour,\n Vous avez atteint le seuil minimal de {item.product_designation}\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', "mounir.benhalima@tayplast-dz.com", None, None, None, None, None)
                                #     except:
                                #         pass
                            else:
                                item.quantity -= order_item.quantity
                                # if item.quantity < item.threshold:
                                #     try:
                                #         email(request, "Seuil Minimal Atteint", f'Bonjour,\n Vous avez atteint le seuil minimal de {item.product_designation}\n Seuil minimal : {item.threshold}\n Quantité en Stock actuellement : {item.quantity}\n\n\n\t S.A.R.L TayPlast', "mounir.benhalima@tayplast-dz.com", None, None, None, None, None)
                                #     except:
                                #         pass
                        elif order.user.profile.job_position.name == 'Mélangeur':                    
                            item.quantity_workshop -= order_item.quantity
                try:
                    item.save()
                    # if item.quantity_workshop < 0:
                    #     try:
                    #         email(request, "ATTENTION !", f"Bonjour,\n {order.user} vient d'effectuer un mélange résultant un stock atelier négatif de {item.product_designation} qui est actuellement : {item.quantity_workshop} Kg\n\n Il est nécessaire d'effectuer une rectification de la matière en question.\n\n\n\t S.A.R.L TayPlast", "mounir.benhalima@tayplast-dz.com", "m.lazreug@tayplast-dz.com", None, None, None, None)
                    #     except:
                    #         pass
                    # elif item.quantity < 0:
                    #     try:
                    #         email(request, "ATTENTION !", f"Bonjour,\n {order.user} vient d'effectuer une opération résultant un stock négatif de {item.product_designation} qui est actuellement : {item.quantity} \n\n Il est nécessaire d'effectuer une rectification.\n\n\n\t S.A.R.L TayPlast", "mounir.benhalima@tayplast-dz.com", "m.lazreug@tayplast-dz.com", None, None, None, None)
                    #     except:
                    #         pass
                    # elif item.external_quantity < 0:
                    #     try:
                    #         email(request, "ATTENTION !", f"Bonjour,\n {order.user} vient d'effectuer une opération résultant un stock externe négatif de {item.product_designation} qui est actuellement : {item.external_quantity} \n\n Il est nécessaire d'effectuer une rectification.\n\n\n\t S.A.R.L TayPlast", "mounir.benhalima@tayplast-dz.com", "m.lazreug@tayplast-dz.com", None, None, None, None)
                    #     except:
                    #         pass
                except IntegrityError:
                        error_message = f"Quantité '{item.product_designation}' Non Disponible En Stock"
                        messages.error(request, error_message)
                        return redirect(reverse_lazy('stock-manager:order-summary'))
            order.ordered = True
            order.save()
            if order.user.profile.job_position.name == 'Mélangeur':
                return redirect(reverse_lazy("production:index-mixing"))
            if order.user.profile.job_position.name == 'Gestionnaire de Stock':
                return redirect(order.get_absolute_url())


    except ObjectDoesNotExist:
        return redirect(reverse_lazy('stock-manager:index'))


@login_required
def remove_from_cart(request, identifier):
    
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    
    if order_qs.exists():
        order = order_qs[0]
        if order.category == "Cordon":
            item = get_object_or_404(OrderHandle, identifier = identifier)
            
            order.handles.remove(item)
            item.delete()
            if order.handles.count() == 0:
                order.delete()
                return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

        elif order.category == "Labelling":
            item = get_object_or_404(OrderLabelling, identifier = identifier)
            order.labellings.remove(item)
            item.delete()
            if order.labellings.count() == 0:
                order.delete()
                return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

        elif order.category == "Emballage":
            item = get_object_or_404(OrderPackage, identifier = identifier)
            order.packages.remove(item)
            item.delete()
            if order.packages.count() == 0:
                order.delete()
                return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

        elif order.category == "Scotch":
            item = get_object_or_404(OrderTape, identifier = identifier)
            order.tapes.remove(item)
            item.delete()
            if order.tapes.count() == 0:
                order.delete()
                return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

        elif order.category == "Pièce de Rechange":
            item = get_object_or_404(OrderSparePart, identifier = identifier)
            order.parts.remove(item)
            item.delete()
            if order.parts.count() == 0:
                order.delete()
                return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

        else:
            item = get_object_or_404(OrderItem, identifier = identifier)
            order.items.remove(item)
            item.delete()
            if order.items.count() == 0:
                if order.user.profile.job_position.name == "Mélangeur":
                    try:
                        production = Production.objects.get(ref_code = order.ref_code)
                        production.delete()
                        if order.machine is not None:
                            order.machine.state = "FREE"
                            order.machine.save()
                    except:
                        pass
                    order.delete()
                    return redirect("production:index-mixing")
                elif order.user.profile.job_position.name == "Gestionnaire de Stock":
                    order.delete()
                    return redirect("stock-manager:index")
            info_message = f"{item} a été supprimé de la commande."
            messages.info(
                request, info_message)
            return redirect("stock-manager:order-summary")

    else:
        messages.info(request, "Vous n'avez aucune commande active")
        return redirect("stock-manager:order-summary")


class OrderList(ListView):
    queryset = Order.objects.filter(ordered = True)
    template_name = 'stock_manager/list/orders_list.html'
    paginate_by = 10


class OrderDetail(DetailView):
    template_name = 'stock_manager/detail/order_detail.html'
    model = Order
    # slug_field = 'slug'

    def get_object(self, **kwargs):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Order, slug=_slug)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        try:
            try:
                try:
                    try:
                        try:
                            context['category'] = Order.objects.filter(
                                slug=self.kwargs.get('slug'))[0].items.first().item.slug.split('-')[0]
                        except:
                            context['category'] = Order.objects.filter(
                                slug=self.kwargs.get('slug'))[0].handles.first().item.slug.split('-')[0]
                    except:
                        context['category'] = Order.objects.filter(
                                slug=self.kwargs.get('slug'))[0].tapes.first().item.slug.split('-')[0]
                except:
                    context['category'] = Order.objects.filter(
                            slug=self.kwargs.get('slug'))[0].packages.first().item.slug.split('-')[0]
            except:
                context['category'] = Order.objects.filter(
                    slug=self.kwargs.get('slug'))[0].labellings.first().item.slug.split('-')[0]
        except:
            context['category'] = Order.objects.filter(
                slug=self.kwargs.get('slug'))[0].parts.first().item.slug.split('-')[0]
        # Add in a QuerySet of all the books
        return context


def email(request, object, content, email, email2, email3, email4, email5, email6):
    email = EmailMessage(object, content, to=[email, email2, email3, email4, email5, email6])
    email.send()
    return redirect(request.META.get('HTTP_REFERER'))


def stock_movement(request, slug):
    order = get_object_or_404(Order, slug=slug)
    template = loader.get_template('invoices/invoice.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "order_list": order,

    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (order.ref_code)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def stock_status(request, category):
    product_type = category
    product_list = None
    if product_type == 'rawmatter':
        product_list = RawMatter.objects.all()
    elif product_type == 'coiltype':
        product_list = CoilType.objects.all()
        for i in range(product_list.__len__()):
            product_list[i].calculated_quantity_stock = product_list[i].quantity_stock()
            product_list[i].calculated_weight_stock = product_list[i].weight_stock()
    elif product_type == 'finishedproducttype':
        product_list = FinishedProductType.objects.exclude(name__name = "film").all()
    elif product_type == 'handle':
        product_list = Handle.objects.all()
    elif product_type == 'labelling':
        product_list = Labelling.objects.all()
    elif product_type == 'package':
        product_list = Package.objects.all()
    elif product_type == 'tape':
        product_list = Tape.objects.all()
    elif product_type == 'part':
        product_list = SparePart.objects.all()  
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    template = loader.get_template('invoices/stock_status.html')
    context = {
        "user": request.user,
        "company": company,
        "product_list": product_list,
        "category": category,
    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/stock_status.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (timezone.now())
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def stock_workshop_status(request, category):
    product_type = category
    product_list = None
    if product_type == 'rawmatter':
        product_list = RawMatter.objects.all()
    elif product_type == 'coiltype':
        product_list = CoilType.objects.all()
    elif product_type == 'finishedproducttype':
        product_list = FinishedProductType.objects.exclude(name__name = "film").all()
    elif product_type == 'handle':
        product_list = Handle.objects.all()
    elif product_type == 'labelling':
        product_list = Labelling.objects.all()
    elif product_type == 'package':
        product_list = Package.objects.all()
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    template = loader.get_template('invoices/workshop_stock_status.html')
    context = {
        "user": request.user,
        "company": company,
        "product_list": product_list,
        "category": category,
    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/workshop_stock_status.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (timezone.now())
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


@login_required(login_url=reverse_lazy('login'))
def trash_validation(request):
    trashes = Trash.objects.filter(state="PENDING")
    trashes_total = 0
    for t in trashes.all():
        trashes_total += t.weight
    if request.method == "POST":
        difference = 0
        weight = float(request.POST.get("weight"))
        trash_slug = request.POST.get("get_trash")
        trash = get_object_or_404(Trash, slug = trash_slug)
        if trash.state == "PENDING":
            difference = weight - trash.weight
            trash.state = "VALIDATED"
            trash.weight = weight
            trash.save()
            if difference < 0:
                correction = TrashCorrection(date = timezone.now(), user = request.user, trash = trash, difference = difference, type_difference = "NEGATIVE")
                correction.save()
            elif difference > 0:
                correction = TrashCorrection(date = timezone.now(), user = request.user, trash = trash, difference = difference, type_difference = "POSITIVE")
                correction.save()
        else:
            messages.error(request, "Déchet Déjà Validé")
            return render(request,'stock_manager/list/trash.html',context={'object_list':trashes, 'trashes_total':trashes_total})

    return render(request,'stock_manager/list/trash.html',context={'object_list':trashes, 'trashes_total':trashes_total})

def trashout_invoice(request, ref):
    trashout = get_object_or_404(TrashOut, ref=ref)
    template = loader.get_template('invoices/trashout_invoice.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "trashout": trashout,

    }
    html = template.render(context)
    pdf = render_to_pdf('invoices/trashout_invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" % (trashout.ref)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
  
class GeneralTrashCreateView(View):
    model = Trash
    template_name = 'stock_manager/general_trash.html' 
    success_url = reverse_lazy('stock-manager:general-trash')
    
    def get(self, request, *arg, **kwargs):
        form = GeneralTrashForm()
        context= {
        'form':form,
        }
        return render(self.request, 'stock_manager/general_trash.html', context)

    def post(self, request, *args, **kwargs):

        form = GeneralTrashForm(request.POST)
        
        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                trash_type = form.trash_type
                machine = form.machine
                weight = form.weight
                comment = form.comment
                company = Company.objects.get(name = "Ln Plast")
                ref = get_random_string(15)
                trash = Trash(ref = ref, date = timezone.now(), weight = weight, machine = machine, trash_type = trash_type, whereabouts = company, state = "VALIDATED", comment = comment )
                trash.save()
                return redirect (self.success_url)
            else:
                pass

class TrashOutView(View):
    model = TrashOut
    template_name = 'stock_manager/trash_out.html' 
    success_url = reverse_lazy('stock-manager:trash-out')
    
    def get(self, request, *arg, **kwargs):
        form = TrashOutForm()
        
        high_trashes_in = Trash.objects.filter(trash_type="HAUTE_DENSITE", state="VALIDATED")
        total_trash_high = 0
        for t in high_trashes_in.all():
            total_trash_high += t.weight
        
        high_trashes_out = TrashOut.objects.filter(trash_type="HAUTE_DENSITE")
        for t in high_trashes_out.all():
            total_trash_high -= t.weight
        

        low_trashes_in = Trash.objects.filter(trash_type="BASSE_DENSITE", state="VALIDATED")
        total_trash_low = 0
        for t in low_trashes_in.all():
            total_trash_low += t.weight
        
        low_trashes_out = TrashOut.objects.filter(trash_type="BASSE_DENSITE")
        for t in low_trashes_out.all():
            total_trash_low -= t.weight

        context= {
        'total_trash_high':total_trash_high,
        'total_trash_low':total_trash_low,
        'form':form,
        }
        return render(self.request, 'stock_manager/trash_out.html', context)

    def post(self, request, *args, **kwargs):
        tmp = 0
        form = TrashOutForm(request.POST)
        
        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                trash_type = form.trash_type
                weight = float(form.weight)
                destination = form.destination
                
                high_trashes_in = Trash.objects.filter(trash_type="HAUTE_DENSITE", state="VALIDATED")
                total_trash_high = 0
                for t in high_trashes_in.all():
                    total_trash_high += t.weight
                
                high_trashes_out = TrashOut.objects.filter(trash_type="HAUTE_DENSITE")
                for t in high_trashes_out.all():
                    total_trash_high -= t.weight
                
        
                low_trashes_in = Trash.objects.filter(trash_type="BASSE_DENSITE", state="VALIDATED")
                total_trash_low = 0
                for t in low_trashes_in.all():
                    total_trash_low += t.weight
                
                low_trashes_out = TrashOut.objects.filter(trash_type="BASSE_DENSITE")
                for t in low_trashes_out.all():
                    total_trash_low -= t.weight


                if trash_type == "HAUTE_DENSITE" and weight > total_trash_high:
                    messages.error(request, "Poids Déchet non disponible en stock !")
                    return redirect(self.request.META.get('HTTP_REFERER'))
                elif trash_type == "BASSE_DENSITE" and weight > total_trash_low:
                    messages.error(request, "Poids Déchet non disponible en stock !")
                    return redirect(self.request.META.get('HTTP_REFERER'))
                ref = get_random_string(15)
                trashout = TrashOut(ref = ref, user = request.user, date = timezone.now(), weight = weight, trash_type = trash_type, destination = destination )
                trashout.save()
                
                return redirect (self.success_url)
            else:
                pass

class TrashInRecapView(ListView):

    template_name = 'stock_manager/list/trash_in_recap.html'

    def get_queryset(self,**kwargs):
        queryset = Trash.objects.filter(state = "VALIDATED")
        return queryset

class TrashOutRecapView(ListView):

    template_name = 'stock_manager/list/trash_out_recap.html'

    def get_queryset(self,**kwargs):
        queryset = TrashOut.objects.all()
        return queryset

def difference_rawmatter_workshop(request):
    quantity = None
    raw_slug = None
    raw = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        raw_slug = request.POST.get("obj")
        raw = RawMatter.objects.get(slug = raw_slug)
        difference = quantity - raw.quantity_workshop
        raw.quantity_workshop = quantity
        raw.save()
        if difference > 0:
            gap = GapRawMatter(user = request.user, date = timezone.now(), difference=difference, type_difference="POSITIVE", rawmatter = raw )
            gap.save()
        elif difference < 0:
            gap = GapRawMatter(user = request.user, date = timezone.now(), difference=difference, type_difference="NEGATIVE", rawmatter = raw )
            gap.save()
        else:
            pass

    return render(request, 'stock_manager/list/stock_workshop.html', context={'object_list': RawMatter.objects.all(), 'category' : 'rawmatter'})

def difference_handle_workshop(request):
    quantity = None
    handle_slug = None
    handle = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        handle_slug = request.POST.get("obj")
        handle = Handle.objects.get(slug = handle_slug)
        difference = quantity - handle.quantity_workshop
        handle.quantity_workshop = quantity
        handle.save()
        if difference > 0:
            gap = GapHandle(user = request.user, date = timezone.now(), difference=difference, type_difference="POSITIVE", handle = handle )
            gap.save()
        elif difference < 0:
            gap = GapHandle(user = request.user, date = timezone.now(), difference=difference, type_difference="NEGATIVE", handle = handle )
            gap.save()
        else:
            pass

    return render(request, 'stock_manager/list/stock_workshop.html', context={'object_list': Handle.objects.all(), 'category' : 'handle'})

def difference_labelling_workshop(request):
    quantity = None
    labelling_slug = None
    labelling = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        labelling_slug = request.POST.get("obj")
        labelling = Labelling.objects.get(slug = labelling_slug)
        difference = quantity - labelling.quantity_workshop
        labelling.quantity_workshop = quantity
        labelling.save()
        if difference > 0:
            gap = GapLabelling(user = request.user, date = timezone.now(), difference=difference, type_difference="POSITIVE", labelling = labelling )
            gap.save()
        elif difference < 0:
            gap = GapLabelling(user = request.user, date = timezone.now(), difference=difference, type_difference="NEGATIVE", labelling = labelling )
            gap.save()
        else:
            pass

    return render(request, 'stock_manager/list/stock_workshop.html', context={'object_list': Labelling.objects.all(), 'category' : 'labelling'})

def difference_package_workshop(request):
    quantity = None
    package_slug = None
    package = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        package_slug = request.POST.get("obj")
        package = Package.objects.get(slug = package_slug)
        difference = quantity - package.quantity_workshop
        package.quantity_workshop = quantity
        package.save()
        if difference > 0:
            gap = GapPackage(user = request.user, date = timezone.now(), difference=difference, type_difference="POSITIVE", package = package )
            gap.save()
        elif difference < 0:
            gap = GapPackage(user = request.user, date = timezone.now(), difference=difference, type_difference="NEGATIVE", package = package )
            gap.save()
        else:
            pass

    return render(request, 'stock_manager/list/stock_workshop.html', context={'object_list': Package.objects.all(), 'category' : 'package'})

def rawmatter_loss(request):
    quantity = None
    raw_slug = None
    raw = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        raw_slug = request.POST.get("raw")
        raw = RawMatter.objects.get(slug = raw_slug)
        qt = raw.quantity - quantity
        raw.quantity = qt
        raw.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity,cause = cause, rawmatter = raw, loss_type ="STOCK")
        loss.save()

    return render(request, 'stock_manager/list/rawmatter_loss.html', context={'object_list': RawMatter.objects.all()})

def workshop_rawmatter_loss(request):
    quantity = None
    raw_slug = None
    raw = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        raw_slug = request.POST.get("raw")
        raw = RawMatter.objects.get(slug = raw_slug)
        qt = raw.quantity_workshop - quantity
        raw.quantity_workshop = qt
        raw.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity, cause = cause, rawmatter = raw, loss_type="WORKSHOP")
        loss.save()

    return render(request, 'stock_manager/list/workshop_rawmatter_loss.html', context={'object_list': RawMatter.objects.filter(quantity_workshop__gt = 0)})

def labelling_loss(request):
    quantity = None
    lab_slug = None
    lab = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        lab_slug = request.POST.get("lab")
        lab = Labelling.objects.get(slug = lab_slug)
        qt = lab.quantity - quantity
        lab.quantity = qt
        lab.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity, cause = cause, labelling = lab, loss_type="STOCK")
        loss.save()

    return render(request, 'stock_manager/list/labelling_loss.html', context={'object_list': Labelling.objects.all()})

def workshop_labelling_loss(request):
    quantity = None
    lab_slug = None
    lab = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        lab_slug = request.POST.get("lab")
        lab = Labelling.objects.get(slug = lab_slug)
        qt = lab.quantity_workshop - quantity
        lab.quantity_workshop = qt
        lab.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity, cause = cause, labelling = lab, loss_type="WORKSHOP")
        loss.save()

    return render(request, 'stock_manager/list/workshop_labelling_loss.html', context={'object_list': Labelling.objects.filter(quantity_workshop__gt = 0)})


def package_loss(request):
    quantity = None
    pack_slug = None
    pack = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        pack_slug = request.POST.get("pack")
        pack = Package.objects.get(slug = pack_slug)
        qt = pack.quantity - quantity
        pack.quantity = qt
        pack.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity, cause = cause, package = pack, loss_type="STOCK")
        loss.save()

    return render(request, 'stock_manager/list/package_loss.html', context={'object_list': Package.objects.all()})

def workshop_package_loss(request):
    quantity = None
    pack_slug = None
    pack = None
    if request.method == "POST":
        quantity = float(request.POST.get("quantity"))
        cause = request.POST.get("cause")
        pack_slug = request.POST.get("pack")
        pack = Package.objects.get(slug = pack_slug)
        qt = pack.quantity_workshop - quantity
        pack.quantity_workshop = qt
        pack.save()
        loss = Loss(date = timezone.now(), user = request.user, quantity = quantity, cause = cause, package = pack, loss_type="WORKSHOP")
        loss.save()

    return render(request, 'stock_manager/list/workshop_package_loss.html', context={'object_list': Package.objects.filter(quantity_workshop__gt =0 )})


class RecapPage(View):
    template_name = 'stock_manager/recap_page.html'

    def get(self, request):
        return render(request, "stock_manager/recap_page.html")


def recap(request):
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

        company = Company.objects.filter(name ="Ln Plast")[0]
        ####################### Pointage #######################
    
        product_orders = Order.objects.filter(category = "Produit Fini") 
        matter_orders = Order.objects.filter(category = "Matière Première", user__profile__job_position__name = "Gestionnaire de Stock")
        product_orders = product_orders.filter(ordered_date__gte = start_date)
        product_orders = product_orders.filter(ordered_date__lte = end_date)
        matter_orders = matter_orders.filter(ordered_date__gte = start_date)
        matter_orders = matter_orders.filter(ordered_date__lte = end_date)

        high_trash_in_total = 0
        low_trash_in_total = 0
        unit_weight = 0
        high_trash_in_total_weight = 0
        low_trash_in_total_weight = 0

        raw = RawMatter.objects.all()

        for i in range(raw.__len__()):
            raw[i].calculated_our_quantity_brought = raw[i].our_quantity_brought(start_date, end_date)
            raw[i].calculated_our_quantity_taken = raw[i].our_quantity_taken(start_date, end_date)

        for i in matter_orders.filter(intern_user = None, type_order = "STOCK_ENTRY"):
            for item in i.items.all():
                if item.item.name.name == "polyéthylène recyclé":
                    if item.item.type_name == "HAUTE_DENSITE":
                        high_trash_in_total += item.quantity
                        unit_weight = item.item.weight
                    elif item.item.type_name == "BASSE_DENSITE":
                        low_trash_in_total += item.quantity
                        unit_weight = item.item.weight
        
        high_trash_in_total_weight = high_trash_in_total * unit_weight
        low_trash_in_total_weight = low_trash_in_total * unit_weight
        trashouts = TrashOut.objects.filter(date__gte = start_date)
        trashouts = trashouts.filter(date__lte = end_date)

        high_trash_out_total = 0
        low_trash_out_total = 0

        for i in trashouts.all():
            if i.trash_type == "HAUTE_DENSITE":
                high_trash_out_total += i.weight
            elif i.trash_type == "BASSE_DENSITE":
                low_trash_out_total += i.weight

        coils = Coil.objects.exclude(supplier = None).all()
        coils = coils.filter(creation_date__gte = start_date)
        coils = coils.filter(creation_date__lte = end_date)

        coils_number = coils.count()
        coils_weight = 0

        for i in coils.all():
            coils_weight += i.weight

        template = loader.get_template('production/recap.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "user": request.user,
            "company": company,
            "product_orders": product_orders,
            "matter_orders": matter_orders,
            "coils":coils,
            "raw":raw,
            "coils_number":coils_number,
            "coils_weight":coils_weight,
            "high_trash_in_total" : high_trash_in_total,
            "low_trash_in_total" : low_trash_in_total,
            "high_trash_in_total_weight" : high_trash_in_total_weight,
            "low_trash_in_total_weight" : low_trash_in_total_weight,
            "high_trash_out_total" : high_trash_out_total,
            "low_trash_out_total" : low_trash_out_total,
        }
        html = template.render(context)
        pdf = render_to_pdf('stock_manager/recap.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "recap%s.pdf" % (timezone.now())
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        template = loader.get_template('production/reporting.html')