import os, glob, shutil, sys

from PIL import Image

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.template import loader, Context
from django.db.models import Sum
from django.db.models import Count
import math
from django.db.models import F
from django.contrib.auth.models import User

# from barcode import EAN13

from django.utils.crypto import get_random_string
from django.core.mail import send_mail, EmailMessage
from StockManager.views import email
from django.utils.dateparse import parse_date

from datetime import date
from datetime import datetime

from decimal import Decimal

from reportlab.pdfgen import canvas
import io
from django.http import FileResponse

from StockManager.utils import render_to_pdf

from django.db.models import Q

from django.views.generic import (
    TemplateView,
    View,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView
)
from . models import Production, Correction, TrashCorrection, GapRawMatter, Cancellation, HandleConsumption, LabellingConsumption, PackageConsumption, InkConsumption
from Profile.models import HolidayRequest, Point, Salary, Profile, JobPosition
from Profile.forms import HolidayRequestForm, PointForm
from Machine.models import Machine, MachineStop
from .forms import ExtrusionForm, ShapingForm, CoilDetailForm, ShapingForm, PrintingForm, FinishedProductForm, ExtrusionTrashForm, PrintingTrashForm, ShapingTrashForm, GeneralTrashForm, HandleConsumptionForm,LabellingConsumptionForm, ExtrusionMachineStopForm, PrintingMachineStopForm, ShapingMachineStopForm, MixingMachineStopForm, InkConsumptionForm, CoilForm, ProductionForm
from Product.models import Range, Color, Flavor, Product, RawMatter, Color,CombinedRange, Coil, CoilType, FinishedProductType, Trash, Handle, Package, Labelling, SparePart
from StockManager.models import Order, TrashOut, Loss, SparePartConsumption, CoilSale
from Company.models import Company
from Contact.models import Contact

def is_valid_queryparam(param):
    return param != '' and param is not None


def filter_order(request):
    qs = Order.objects.filter(machine=None)

    id_user = request.GET.get('_id_user')
    id_client = request.GET.get('_id_client')
    id_supplier = request.GET.get('_id_supplier')
    id_intern_user = request.GET.get('_id_intern_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    id_company = request.GET.get('_id_company')
    ref = request.GET.get('_ref')
    stock_entry = request.GET.get('_stock_entry')
    stock_out = request.GET.get('_stock_out')
    stock_return = request.GET.get('_stock_return')
    internal = request.GET.get('_internal')
    external = request.GET.get('_external')
    internal_stock = request.GET.get('_internal_stock')
    external_stock = request.GET.get('_external_stock')
    category = request.GET.get('_category')
    _is_ordered = request.GET.get('_is_ordered')
    _is_not_ordered = request.GET.get('_is_not_ordered')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(id_company):
        qs = qs.filter(Q(company__name__icontains=id_company))

    if is_valid_queryparam(id_client):
        qs = qs.filter(Q(client__first_name__icontains=id_client)
                       | Q(client__last_name__icontains=id_client))

    if is_valid_queryparam(id_supplier):
        qs = qs.filter(Q(supplier__first_name__icontains=id_supplier)
                       | Q(supplier__last_name__icontains=id_supplier))

    if is_valid_queryparam(id_intern_user):
        qs = qs.filter(Q(intern_user__first_name__icontains=id_intern_user)
                       | Q(intern_user__last_name__icontains=id_intern_user))

    if is_valid_queryparam(date_min):
        qs = qs.filter(ordered_date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(ordered_date__lte=date_max)

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code=ref))

    if is_valid_queryparam(category):
        qs = qs.filter(category__icontains=category)

    if _is_ordered == 'on':
        qs = qs.filter(ordered=True)
    if _is_not_ordered == 'on':
        qs = qs.filter(ordered=False)

    if internal == 'on':
        qs = qs.filter(type_consumption="INTERNAL")
    if external == 'on':
        qs = qs.filter(type_order="STOCK_OUT" , type_consumption="EXTERNAL")
    
    if internal_stock == 'on':
        qs = qs.filter(external_stock = False)
    if external_stock == 'on':
        qs = qs.filter(external_stock = True)

    if stock_entry == 'on':
        qs = qs.filter(type_order="STOCK_ENTRY")
    if stock_out == 'on':
        qs = qs.filter(type_order="STOCK_OUT")
    if stock_return == 'on':
        qs = qs.filter(type_order="STOCK_RETURN")

    return qs
#

def filter_mixing(request):
    qs = Order.objects.exclude(machine=None).all()

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code__icontains=ref))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))

    if is_valid_queryparam(date_min):
        qs = qs.filter(ordered_date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(ordered_date__lte=date_max)

    return qs
#


def filter_printing(request):
    qs = Production.objects.filter(process_type = "PRINTING")

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    is_finished = request.GET.get('_is_finished')
    is_not_finished = request.GET.get('_is_not_finished')
    id_coil = request.GET.get('_id_coil')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code__icontains=ref))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))
    
    if is_valid_queryparam(id_coil):
        qs = qs.filter(Q(coil__product_designation__icontains=id_coil))    

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if is_finished == 'on':
        qs = qs.filter(state="FINISHED")
    if is_not_finished == 'on':
        qs = qs.filter(state="PENDING")

    return qs
#

def filter_extrusion(request):
    qs = Production.objects.filter(process_type = "EXTRUSION")

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    is_finished = request.GET.get('_is_finished')
    is_not_finished = request.GET.get('_is_not_finished')
    id_coil = request.GET.get('_id_coil')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code__icontains=ref))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))
    
    if is_valid_queryparam(id_coil):
        qs = qs.filter(Q(coil__product_designation__icontains=id_coil))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if is_finished == 'on':
        qs = qs.filter(state="FINISHED")
    if is_not_finished == 'on':
        qs = qs.filter(state="PENDING")

    return qs
#

def filter_shaping(request):
    qs = Production.objects.filter(process_type = "SHAPING")

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    is_finished = request.GET.get('_is_finished')
    is_not_finished = request.GET.get('_is_not_finished')
    id_coil = request.GET.get('_id_coil')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code__icontains=ref))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))
    
    if is_valid_queryparam(id_coil):
        qs = qs.filter(Q(coil__product_designation__icontains=id_coil))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if is_finished == 'on':
        qs = qs.filter(state="FINISHED")
    if is_not_finished == 'on':
        qs = qs.filter(state="PENDING")

    return qs
#

def filter_finished_product(request):
    qs = Production.objects.filter(process_type = "FINISHED_PRODUCT")

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    id_product = request.GET.get('_id_product')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    is_finished = request.GET.get('_is_finished')
    is_not_finished = request.GET.get('_is_not_finished')
    gain = request.GET.get('_gain')
    loss = request.GET.get('_loss')
    id_quantity = request.GET.get('_id_quantity')

    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user)
                       | Q(user2__first_name__icontains=id_user)
                       | Q(user2__last_name__icontains=id_user)
                       | Q(user3__first_name__icontains=id_user)
                       | Q(user3__last_name__icontains=id_user))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref_code__icontains=ref))

    if is_valid_queryparam(id_product):
        qs = qs.filter(Q(product__product_designation__icontains=id_product)) 

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if is_valid_queryparam(id_quantity):
        qs = qs.filter(quantity_produced=id_quantity)

    if is_finished == 'on':
        qs = qs.filter(state="FINISHED")
    if is_not_finished == 'on':
        qs = qs.filter(state="PENDING")
    
    if gain == 'on':
        qs = qs.annotate(difference=F('weight')-F('ideal_weight')).filter(difference__lte=0)
    if loss == 'on':
       qs = qs.annotate(difference=F('weight')-F('ideal_weight')).filter(difference__gt=0)

    return qs
#

def filter_coil(request):
    now = timezone.now()
    if now.month == 1:
        month = 11
        year = now.year - 1
    elif now.month == 2:
        month = 12
        year = now.year - 1
    else:
        month = now.month - 2
        year = now.year

    now = now.replace(day = 1, month=month, year = year, hour = 6)

    qs = Coil.objects.filter(creation_date__gte = now)

    id_user = request.GET.get('_id_user')
    id_printer = request.GET.get('_id_printer')
    id_shaper = request.GET.get('_id_shaper')

    id_extrusion_machine = request.GET.get('_id_extrusion_machine')
    id_printing_machine = request.GET.get('_id_printing_machine')
    id_shaping_machine = request.GET.get('_id_shaping_machine')

    creation_date_min = request.GET.get('creation_date_min')
    creation_date_max = request.GET.get('creation_date_max')

    printing_date_min = request.GET.get('printing_date_min')
    printing_date_max = request.GET.get('printing_date_max')

    shaping_date_min = request.GET.get('shaping_date_min')
    shaping_date_max = request.GET.get('shaping_date_max')

    printed = request.GET.get('_printed')
    not_printed = request.GET.get('_not_printed')

    defective = request.GET.get('_defective')
    normal = request.GET.get('_normal')

    external = request.GET.get('_external')

    destroyed = request.GET.get('_destroyed')
    not_destroyed = request.GET.get('_not_destroyed')

    pending_extrusion = request.GET.get('_pending_extrusion')
    in_stock = request.GET.get('_in_stock')
    pending_printing = request.GET.get('_pending_printing')
    pending_shaping = request.GET.get('_pending_shaping')
    in_quarantine = request.GET.get('_in_quarantine')
    consumed = request.GET.get('_consumed')
    sold = request.GET.get('_sold')
    cut = request.GET.get('_cut')
    derived = request.GET.get('_derived')

    ref_coil = request.GET.get("_id_coil")

    weight = request.GET.get('_id_weight')
    micronnage = request.GET.get('_id_micronnage')

    parent = request.GET.get('_id_children_of')

    cw1 = request.GET.get('_id_cw1')
    cw2 = request.GET.get('_id_cw2')
    cw3 = request.GET.get('_id_cw3')
    cwm = request.GET.get('_id_cwm')


    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(id_printer):
        qs = qs.filter(Q(printer__first_name__icontains=id_printer)
                       | Q(printer__last_name__icontains=id_printer))

    if is_valid_queryparam(id_shaper):
        qs = qs.filter(Q(shaper__first_name__icontains=id_shaper)
                       | Q(shaper__last_name__icontains=id_shaper))



    if is_valid_queryparam(id_extrusion_machine):
        qs = qs.filter(Q(extrusion_machine__designation__icontains=id_extrusion_machine))


    if is_valid_queryparam(id_printing_machine):
        qs = qs.filter(Q(printing_machine__designation__icontains=id_printing_machine)) 

    if is_valid_queryparam(id_shaping_machine):
        qs = qs.filter(Q(shaping_machine__designation__icontains=id_shaping_machine))


    if is_valid_queryparam(parent):
        qs = qs.filter(Q(parent__product_designation__icontains=parent))



    if is_valid_queryparam(creation_date_min):
        qs = qs.filter(creation_date__gte=creation_date_min)
    if is_valid_queryparam(creation_date_max):
        qs = qs.filter(creation_date__lte=creation_date_max)
    
    if is_valid_queryparam(printing_date_min):
        qs = qs.filter(printing_date__gte=printing_date_min)
    if is_valid_queryparam(printing_date_max):
        qs = qs.filter(printing_date__lte=printing_date_max)

    if is_valid_queryparam(shaping_date_min):
        qs = qs.filter(shaping_date__gte=shaping_date_min)
    if is_valid_queryparam(shaping_date_max):
        qs = qs.filter(shaping_date__lte=shaping_date_max)


    if printed == 'on':
        qs = qs.filter(printed="PRINTED")
    if not_printed == 'on':
        qs = qs.filter(printed="NOT_PRINTED")

    if defective == 'on':
        qs = qs.filter(defective="DEFECTIVE")
    if normal == 'on':
        qs = qs.filter(defective="NON_DEFECTIVE")

    if external == 'on':
        qs = qs.exclude(supplier=None)


    if pending_extrusion == 'on':
        qs = qs.filter(status="PENDING_EXTRUSION")
    if in_stock == 'on':
        qs = qs.filter(status="IN_STOCK")
    if pending_printing == 'on':
        qs = qs.filter(status="PENDING_PRINTING")
    if pending_shaping == 'on':
        qs = qs.filter(status="PENDING_SHAPING")
    if in_quarantine == 'on':
        qs = qs.filter(status="QUARANTINE")
    if consumed == 'on':
        qs = qs.filter(status="CONSUMED")
    if sold == 'on':
        qs = qs.filter(status="SOLD")
    if cut == 'on':
        qs = qs.filter(status="CUT")
    if derived == 'on':
        qs = qs.filter(is_sub=True)
    
    if destroyed == 'on':
        qs = qs.filter(destroyed=True)
    if not_destroyed == 'on':
        qs = qs.filter(status = "TO_BE_DESTROYED", destroyed=False)

    if is_valid_queryparam(ref_coil):
        qs = qs.filter(product_designation__icontains=ref_coil)
    

    if is_valid_queryparam(weight):
        qs = qs.filter(weight=weight)
    if is_valid_queryparam(micronnage):
        qs = qs.filter(micronnage=micronnage)

    if is_valid_queryparam(cw1):
        qs = qs.filter(cw1=cw1)
    if is_valid_queryparam(cw2):
        qs = qs.filter(cw2=cw2)
    if is_valid_queryparam(cw3):
        qs = qs.filter(cw3=cw3)
    if is_valid_queryparam(cwm):
        qs = qs.filter(cwm=cwm)
        
    return qs
#

def filter_trash(request):
    qs = Trash.objects.all()
    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    weight = request.GET.get('_id_weight')
    id_high = request.GET.get('_id_high')
    id_low = request.GET.get('_id_low')
    is_validated = request.GET.get('_is_validated')
    is_not_validated = request.GET.get('_is_not_validated')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref__icontains=ref))


    if is_valid_queryparam(weight):
        qs = qs.filter(Q(weight=weight))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if id_high == 'on':
        qs = qs.filter(trash_type="HAUTE_DENSITE")
    if id_low == 'on':
        qs = qs.filter(trash_type="BASSE_DENSITE")
    
    if is_validated == 'on':
        qs = qs.filter(state="VALIDATED")
    if is_not_validated == 'on':
        qs = qs.filter(state="PENDING")

    return qs
#

def filter_trashout(request):
    qs = TrashOut.objects.all()

    id_user = request.GET.get('_id_user')
    ref = request.GET.get('_ref')
    id_machine = request.GET.get('_id_machine')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    weight = request.GET.get('_id_weight')
    id_high = request.GET.get('_id_high')
    id_low = request.GET.get('_id_low')
    is_validated = request.GET.get('_is_validated')
    is_not_validated = request.GET.get('_is_not_validated')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(ref):
        qs = qs.filter(Q(ref__icontains=ref))

    if is_valid_queryparam(id_machine):
        qs = qs.filter(Q(machine__name__icontains=id_machine))


    if is_valid_queryparam(weight):
        qs = qs.filter(Q(weight=weight))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if id_high == 'on':
        qs = qs.filter(trash_type="HAUTE_DENSITE")
    if id_low == 'on':
        qs = qs.filter(trash_type="BASSE_DENSITE")
    
    if is_validated == 'on':
        qs = qs.filter(state="VALIDATED")
    if is_not_validated == 'on':
        qs = qs.filter(state="PENDING")

    return qs
#


def filter_product_correction(request):
    qs = Correction.objects.all()

    id_user = request.GET.get('_id_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    difference = request.GET.get('_id_difference')
    production = request.GET.get('_id_production')
    positive_difference = request.GET.get('_id_positive_difference')
    negative_difference = request.GET.get('_id_negative_difference')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))


    if is_valid_queryparam(difference):
        qs = qs.filter(Q(difference=difference))
    
    if is_valid_queryparam(production):
        qs = qs.filter(Q(production__ref_code__icontains=production))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if positive_difference == 'on':
        qs = qs.filter(type_difference="POSITIVE")
    if negative_difference == 'on':
        qs = qs.filter(type_difference="NEGATIVE")

    return qs
#


def filter_trash_correction(request):
    qs = TrashCorrection.objects.all()

    id_user = request.GET.get('_id_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    difference = request.GET.get('_id_difference')
    trash = request.GET.get('_id_trash')
    positive_difference = request.GET.get('_id_positive_difference')
    negative_difference = request.GET.get('_id_negative_difference')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))


    if is_valid_queryparam(difference):
        qs = qs.filter(Q(difference=difference))
    
    if is_valid_queryparam(trash):
        qs = qs.filter(Q(trash__ref__icontains=trash))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if positive_difference == 'on':
        qs = qs.filter(type_difference="POSITIVE")
    if negative_difference == 'on':
        qs = qs.filter(type_difference="NEGATIVE")

    return qs
#

def filter_workshop_correction(request):
    qs = GapRawMatter.objects.all()

    id_user = request.GET.get('_id_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    difference = request.GET.get('_id_difference')
    raw = request.GET.get('_id_raw')
    positive_difference = request.GET.get('_id_positive_difference')
    negative_difference = request.GET.get('_id_negative_difference')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))


    if is_valid_queryparam(difference):
        qs = qs.filter(Q(difference=difference))
    
    if is_valid_queryparam(raw):
        qs = qs.filter(Q(rawmatter__product_designation__icontains=raw))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if positive_difference == 'on':
        qs = qs.filter(type_difference="POSITIVE")
    if negative_difference == 'on':
        qs = qs.filter(type_difference="NEGATIVE")

    return qs
#

def filter_cancellation(request):
    qs = Cancellation.objects.all()

    id_user = request.GET.get('_id_user')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    cancellation_type = request.GET.get('_cancellation_type')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(cancellation_type):
        qs = qs.filter(Q(cancellation_type__icontains=cancellation_type))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs
#
def filter_loss(request):
    qs = Loss.objects.all()

    id_user = request.GET.get('_id_user')
    product = request.GET.get('_prod')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    quantity = request.GET.get('_quantity')
    stock = request.GET.get('_stock')
    workshop = request.GET.get('_workshop')

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(quantity):
        qs = qs.filter(Q(quantity=quantity))

    if is_valid_queryparam(product):
        qs = qs.filter(Q(rawmatter__product_designation__icontains=product)
                        | Q(labelling__designation__icontains=product)
                        | Q(package__designation__icontains=product))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if stock == 'on':
        qs = qs.filter(loss_type="STOCK")
    if workshop == 'on':
        qs = qs.filter(loss_type="WORKSHOP")


    return qs
#

def filter_handle(request):
    qs = HandleConsumption.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    handle = request.GET.get('_id_handle')
    quantity = request.GET.get('_id_quantity')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(quantity):
        qs = qs.filter(Q(quantity=quantity))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(handle):
        qs = qs.filter(Q(handle__designation__icontains=handle))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs
#
def filter_labelling(request):
    qs = LabellingConsumption.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    labelling = request.GET.get('_id_labelling')
    quantity = request.GET.get('_id_quantity')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(quantity):
        qs = qs.filter(Q(quantity=quantity))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(labelling):
        qs = qs.filter(Q(labelling__designation__icontains=labelling))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs
#
def filter_package(request):
    qs = PackageConsumption.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    package = request.GET.get('_id_package')
    quantity = request.GET.get('_id_quantity')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(quantity):
        qs = qs.filter(Q(quantity=quantity))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(package):
        qs = qs.filter(Q(package__designation__icontains=package))

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs

def filter_part(request):
    qs = SparePartConsumption.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    part_ref = request.GET.get('_id_part_ref')
    part_name = request.GET.get('_id_part_name')
    quantity = request.GET.get('_id_quantity')
    preventive = request.GET.get('_preventive')
    corrective = request.GET.get('_corrective')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))
    
    if is_valid_queryparam(quantity):
        qs = qs.filter(Q(quantity=quantity))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(part_ref):
        qs = qs.filter(Q(part__ref__icontains=part_ref))
        
    if is_valid_queryparam(part_name):
        qs = qs.filter(Q(part__name__icontains=part_name))

    if preventive == 'on':
        qs = qs.filter(intervention_type="PREVENTIVE")

    if corrective == 'on':
        qs = qs.filter(intervention_type="CORRECTIVE")

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs
#
def filter_machine_stop(request):
    qs = MachineStop.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    duration = request.GET.get('_id_duration')
    electrical_breakdown = request.GET.get('_id_electrical_breakdown')
    mechanical_breakdown = request.GET.get('_id_mechanical_breakdown')
    power = request.GET.get('_id_power')
    teflon = request.GET.get('_id_teflon')
    filterr = request.GET.get('_id_filter')
    blade = request.GET.get('_id_blade')
    clean = request.GET.get('_id_clean')
    other = request.GET.get('_id_other')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(duration):
        qs = qs.filter(duration=duration)

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)

    if electrical_breakdown == 'on':
        qs = qs.filter(cause="ELECTRICAL_BREAKDOWN")
    if mechanical_breakdown == 'on':
        qs = qs.filter(cause="MECHANICAL_BREAKDOWN")
    if power == 'on':
        qs = qs.filter(cause="POWER")
    if teflon == 'on':
        qs = qs.filter(cause="TEFLON")
    if filterr == 'on':
        qs = qs.filter(cause="FILTER")
    if blade == 'on':
        qs = qs.filter(cause="BLADE")
    if clean == 'on':
        qs = qs.filter(cause="CLEAN")
    if other == 'on':
        qs = qs.filter(cause="OTHER")

    return qs
#


def filter_ink_consumption(request):
    qs = InkConsumption.objects.all()

    id_user = request.GET.get('_id_user')
    machine = request.GET.get('_id_machine')
    ink = request.GET.get('_id_ink')
    quantity = request.GET.get('_quantity')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    

    if is_valid_queryparam(id_user):
        qs = qs.filter(Q(user__first_name__icontains=id_user)
                       | Q(user__last_name__icontains=id_user))

    if is_valid_queryparam(machine):
        qs = qs.filter(Q(machine__designation__icontains=machine))

    if is_valid_queryparam(ink):
        qs = qs.filter(Q(ink__product_designation__icontains=ink))

    if is_valid_queryparam(quantity):
        qs = qs.filter(quantity=quantity)

    if is_valid_queryparam(date_min):
        qs = qs.filter(date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(date__lte=date_max)


    return qs
#



class ConsultingOrdersListView(ListView):

    template_name = 'production/order_consulting.html'

    # def get_queryset(self):
    #     qs = filter_order(self.request)
    #     return qs
    def get(self, request, *arg, **kwargs):
        qs = filter_order(self.request)
        total = 0
        for o in qs:    
            total += o.get_total()
        context = {
            'object_list': qs,
            'total': total,
        }
        return render(self.request, 'production/order_consulting.html', context)

class ConsultingMixingListView(ListView):

    template_name = 'production/mixing_consulting.html'

    # def get_queryset(self):
    #     qs = filter_mixing(self.request)
    #     return qs
    def get(self, request, *arg, **kwargs):
        qs = filter_mixing(self.request)
        total_weight = 0
        for p in qs:    
            total_weight += p.get_total()
        context = {
            'object_list': qs,
            'total_weight': total_weight,
        }
        return render(self.request, 'production/mixing_consulting.html', context)

class ConsultingPrintingListView(ListView):

    template_name = 'production/printing_consulting.html'

    def get_queryset(self):
        qs = filter_printing(self.request)
        return qs

class ConsultingExtrusionListView(ListView):

    template_name = 'production/extrusion_consulting.html'

    def get_queryset(self):
        qs = filter_extrusion(self.request)
        return qs

class ConsultingShapingListView(ListView):

    template_name = 'production/shaping_consulting.html'

    def get_queryset(self):
        qs = filter_shaping(self.request)
        return qs

class ConsultingFinishedProductListView(ListView):

    template_name = 'production/finished_product_consulting.html'

    # def get_queryset(self):
    #     qs = filter_finished_product(self.request)
    #     return qs
    def get(self, request, *arg, **kwargs):
        qs = filter_finished_product(self.request)
        for i in range(qs.__len__()):
            qs[i].calculated_weight_difference = qs[i].weight_difference()
        total_weight = 0
        total_packages = 0
        real_total_weight = 0
        total_amount = 0
        for p in qs:
            if p.state =="FINISHED" :
                total_weight += p.quantity_produced * p.product.weight * p.product.roll_package / 1000
            real_total_weight += p.weight
            total_packages += p.quantity_produced
            total_amount += float(p.quantity_produced) * float(p.product.roll_package) * float(p.product.price)

        context = {
            'object_list': qs,
            'total_weight': total_weight,
            'real_total_weight': real_total_weight,
            'total_packages': total_packages,
            'total_amount': total_amount,
        }
        return render(self.request, 'production/finished_product_consulting.html', context)

class ConsultingCoilListView(ListView):

    # template_name = 'production/coil_consulting.html'

    # def get_queryset(self):
    #     qs = filter_coil(self.request)
    # return qs
    def get(self, request, *arg, **kwargs):
        qs = filter_coil(self.request)
        total = 0
        for coil in qs:
            if coil.status != "CUT":
                total += coil.weight
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/coil_consulting.html', context)

class ConsultingTrashListView(ListView):

    # template_name = 'production/trash_consulting.html'

    # def get_queryset(self):
    #     qs = filter_trash(self.request)
    #     return qs
    def get(self, request, *arg, **kwargs):
        qs = filter_trash(self.request)
        total = 0
        for trash in qs:
            if trash.state == "VALIDATED":
                total += trash.weight
        
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

        context = {
            'total_trash_high':total_trash_high,
            'total_trash_low':total_trash_low,
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/trash_consulting.html', context)

class ConsultingTrashOutListView(ListView):
    template_name = 'production/trashout_consulting.html'

    # def get_queryset(self):
    #     qs = filter_trashout(self.request)
    #     return qs
    
    def get(self, request, *arg, **kwargs):
        qs = filter_trashout(self.request)
        total = 0
        for trashout in qs:
            total += trashout.weight
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/trashout_consulting.html', context)


class ConsultingProductCorrectionListView(ListView):
    template_name = 'production/product_correction_consulting.html'

    def get_queryset(self):
        qs = filter_product_correction(self.request)
        return qs

class ConsultingTrashCorrectionListView(ListView):
    template_name = 'production/trash_correction_consulting.html'

    def get_queryset(self):
        qs = filter_trash_correction(self.request)
        return qs

class ConsultingWorkshopCorrectionListView(ListView):
    template_name = 'production/workshop_correction_consulting.html'

    def get_queryset(self):
        qs = filter_workshop_correction(self.request)
        return qs

class ConsultingCancellationListView(ListView):
    template_name = 'production/cancellation_consulting.html'

    def get_queryset(self):
        qs = filter_cancellation(self.request)
        return qs

class ConsultingLossListView(ListView):
    template_name = 'production/loss_consulting.html'

    def get_queryset(self):
        qs = filter_loss(self.request)
        return qs

class ConsultingHandleListView(ListView):
    # template_name = 'production/handle_consulting.html'

    # def get_queryset(self):
    #     qs = filter_handle(self.request)
    #     return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_handle(self.request)
        total = 0
        for h_cons in qs:
            total += h_cons.quantity
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/handle_consulting.html', context)

class ConsultingLabellingListView(ListView):
    # template_name = 'production/labelling_consulting.html'

    # def get_queryset(self):
    #     qs = filter_labelling(self.request)
    #     return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_labelling(self.request)
        total = 0
        for l_cons in qs:
            total += l_cons.quantity
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/labelling_consulting.html', context)

class ConsultingPackageListView(ListView):
    template_name = 'production/package_consulting.html'

    def get_queryset(self):
        qs = filter_package(self.request)
        return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_package(self.request)
        total = 0
        for p_cons in qs:
            total += p_cons.quantity
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/package_consulting.html', context)

class ConsultingPartListView(ListView):
    template_name = 'production/part_consulting.html'

    def get_queryset(self):
        qs = filter_part(self.request)
        return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_part(self.request)
        context = {
            'object_list': qs,
        }
        return render(self.request, 'production/part_consulting.html', context)

class ConsultingMachineStopView(ListView):
    # template_name = 'production/machine_stop_consulting.html'

    # def get_queryset(self):
    #     qs = filter_machine_stop(self.request)
    #     return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_machine_stop(self.request)
        total = 0
        for stop in qs:
            total += stop.hours * 60 + stop.minutes
        
        total_h = total // 60

        total_m = total % 60
        context = {
            'object_list': qs,
            'total': total,
            'total_h': total_h,
            'total_m': total_m,
        }
        return render(self.request, 'production/machine_stop_consulting.html', context)

class ConsultingInkConsumptionView(ListView):
    # template_name = 'production/ink_consumption_consulting.html'

    # def get_queryset(self):
    #     qs = filter_ink_consumption(self.request)
    #     return qs

    def get(self, request, *arg, **kwargs):
        qs = filter_ink_consumption(self.request)
        total = 0
        for i_cons in qs:
            total += i_cons.quantity
        context = {
            'object_list': qs,
            'total': total
        }
        return render(self.request, 'production/ink_consumption_consulting.html', context)


class ConsultingStockStatusView(View):
    template_name = 'production/stock_consulting.html'

    def get(self, request):
        return render(request, "production/stock_consulting.html")

class ConsultingStockWorkshopStatusView(View):
    template_name = 'production/stock_workshop_consulting.html'

    def get(self, request):
        return render(request, "production/stock_workshop_consulting.html")

class IndexView(View):
    template_name = 'production/index.html'

    def get(self, request):
        return render(request, "production/index.html")

class ExtrusionListView(ListView):

    template_name = 'production/pending_extrusion.html'

    def get_queryset(self, **kwargs):
        queryset = Production.objects.filter(state="PENDING", process_type="EXTRUSION")
        return queryset


class HolidayRequestsListView(ListView):

    template_name = 'profile/list/holiday_requests.html'

    def get_queryset(self, **kwargs):
        queryset = HolidayRequest.objects.all()
        return queryset

class HolidayRequestView(View):
    model = HolidayRequest
    template_name = 'profile/holiday_request.html'
    success_url = reverse_lazy('main-index')

    def get(self, request, *arg, **kwargs):
        form = HolidayRequestForm()
        users = User.objects.filter(profile__group = request.user.profile.group)
        context = {
            'form': form,
            'users':users,
        }
        return render(self.request, 'profile/holiday_request.html', context)

    def post(self, request, *args, **kwargs):
        form = HolidayRequestForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                request_date = timezone.now()
                start_date = form.start_date
                end_date = form.end_date
                duration = end_date - start_date
                duration = (duration.total_seconds()/3600 )/24 +1
                if duration < 0:
                    messages.error(request, "Dates érronées")
                    return redirect(request.META.get('HTTP_REFERER'))
                try:
                    user_id = request.POST.get("user")
                    user = User.objects.get(username= user_id)
                except:
                    messages.error(request, "Utilisateur Introuvable")
                    return redirect(request.META.get('HTTP_REFERER'))
                address = form.address
                mobile = form.mobile
                motive = form.motive
                sub = form.substitute

                holiday_request = HolidayRequest(user = user, request_date = request_date, start_date = start_date, end_date = end_date, duration = duration, address = address, mobile = mobile, motive = motive, substitute= sub, state = "PENDING")
                holiday_request.save()

                return redirect(self.success_url)

class ReportingPage(View):
    template_name = 'production/reporting_page.html'

    def get(self, request):
        return render(request, "production/reporting_page.html")

class MiniReportingPage(View):
    template_name = 'production/mini_reporting_page.html'

    def get(self, request):
        return render(request, "production/mini_reporting_page.html")


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

        company = Company.objects.filter(name ="Ln Plast")[0]
        ####################### Pointage #######################
    
        products = FinishedProductType.objects.all()
        for i in range(products.__len__()):
            products[i].calculated_quantity_produced = products[i].quantity_produced(start_date, end_date)
            products[i].calculated_quantity_sold = products[i].quantity_sold(start_date, end_date)
        

        product_combined_ranges = CombinedRange.objects.filter(category = "FINAL_PRODUCT")
        matter_combined_ranges = CombinedRange.objects.filter(category = "RAW_MATTER")

        for i in range(product_combined_ranges.__len__()):
            product_combined_ranges[i].calculated_black_produced = product_combined_ranges[i].black_quantity_produced(start_date, end_date)
            product_combined_ranges[i].calculated_color_produced = product_combined_ranges[i].color_quantity_produced(start_date, end_date)
            product_combined_ranges[i].calculated_main_stock = product_combined_ranges[i].product_main_stock(start_date, end_date)
            product_combined_ranges[i].calculated_external_stock = product_combined_ranges[i].product_external_stock(start_date, end_date)
            
            if product_combined_ranges[i].calculated_black_produced + product_combined_ranges[i].calculated_color_produced != 0:
                product_combined_ranges[i].calculated_black_produced_pourcentage = product_combined_ranges[i].calculated_black_produced / (product_combined_ranges[i].calculated_black_produced + product_combined_ranges[i].calculated_color_produced) * 100
                product_combined_ranges[i].calculated_color_produced_pourcentage = 100 - product_combined_ranges[i].calculated_black_produced_pourcentage
            else:
                product_combined_ranges[i].calculated_black_produced_pourcentage = 0
                product_combined_ranges[i].calculated_color_produced_pourcentage = 0

            product_combined_ranges[i].calculated_black_sold = product_combined_ranges[i].black_quantity_sold(start_date, end_date)
            product_combined_ranges[i].calculated_color_sold = product_combined_ranges[i].color_quantity_sold(start_date, end_date)

            if product_combined_ranges[i].calculated_black_sold + product_combined_ranges[i].calculated_color_sold != 0:
                product_combined_ranges[i].calculated_black_sold_pourcentage = product_combined_ranges[i].calculated_black_sold /(product_combined_ranges[i].calculated_black_sold + product_combined_ranges[i].calculated_color_sold ) * 100
                product_combined_ranges[i].calculated_color_sold_pourcentage = 100 - product_combined_ranges[i].calculated_black_sold_pourcentage
            else:
                product_combined_ranges[i].calculated_black_sold_pourcentage = 0
                product_combined_ranges[i].calculated_color_sold_pourcentage = 0

        for i in range(matter_combined_ranges.__len__()):
            matter_combined_ranges[i].calculated_matter_mixed = matter_combined_ranges[i].quantity_mixed(start_date, end_date)
            matter_combined_ranges[i].calculated_matter_bought = matter_combined_ranges[i].quantity_bought(start_date, end_date)
            matter_combined_ranges[i].calculated_main_stock = matter_combined_ranges[i].raw_main_stock(start_date, end_date)
            matter_combined_ranges[i].calculated_workshop_stock = matter_combined_ranges[i].raw_workshop_stock(start_date, end_date)

        black_production = color_production = black_sales = color_sales = total_sales = total_production = 0
        
        for prod in Production.objects.filter(Q(date__gte = start_date) & Q(date__lte = end_date) & Q(process_type = "FINISHED_PRODUCT")):
            if prod.product.color.name == "noir":
                black_production += prod.quantity_produced
            else:
                color_production += prod.quantity_produced
        
        total_production = black_production + color_production

        if total_production != 0:
            black_production_pourcentage = (black_production/total_production) * 100
            color_production_pourcentage = 100 - black_production_pourcentage
        else:
            black_production_pourcentage = 0
            color_production_pourcentage = 0



        for order in Order.objects.filter(Q(type_order = "STOCK_OUT") & Q(category = "Produit Fini") & Q(ordered_date__gte = start_date) & Q(ordered_date__lte = end_date)):
            for item in order.items.all():
                if item.item.color.name == "noir":
                    black_sales += item.quantity
        
        for order in Order.objects.filter(Q(type_order = "STOCK_OUT") & Q(category = "Produit Fini") & Q(ordered_date__gte = start_date) & Q(ordered_date__lte = end_date)):
            for item in order.items.all():
                if item.item.color.name != "noir":
                    color_sales += item.quantity
        
        total_sales = black_sales + color_sales

        if total_sales != 0:
            black_sales_pourcentage = (black_sales/total_sales) * 100
            color_sales_pourcentage = 100 - black_sales_pourcentage
        else:
            black_sales_pourcentage = 0
            color_sales_pourcentage = 0
        

        raw_matters = RawMatter.objects.all()
        for i in range(raw_matters.__len__()):
            raw_matters[i].calculated_quantity_consumed = raw_matters[i].quantity_consumed(start_date, end_date)
            raw_matters[i].calculated_quantity_brought = raw_matters[i].quantity_brought(start_date, end_date)

        packages = Package.objects.all()
        for i in range(packages.__len__()):
            packages[i].calculated_quantity_consumed = packages[i].quantity_consumed(start_date, end_date)
            packages[i].calculated_quantity_brought = packages[i].quantity_brought(start_date, end_date)

        labellings = Labelling.objects.all()
        for i in range(labellings.__len__()):
            labellings[i].calculated_quantity_consumed = labellings[i].quantity_consumed(start_date, end_date)
            labellings[i].calculated_quantity_brought = labellings[i].quantity_brought(start_date, end_date)
        
        handles = Handle.objects.all()
        for i in range(handles.__len__()):
            handles[i].calculated_quantity_consumed = handles[i].quantity_consumed(start_date, end_date)
            handles[i].calculated_quantity_brought = handles[i].quantity_brought(start_date, end_date)

        coils = CoilType.objects.all()
        for i in range(coils.__len__()):
            coils[i].calculated_quantity_produced = coils[i].quantity_produced(start_date, end_date)
            coils[i].calculated_weight_produced = coils[i].weight_produced(start_date, end_date)
            coils[i].calculated_quantity_shaped = coils[i].quantity_shaped(start_date, end_date)
            coils[i].calculated_weight_shaped = coils[i].weight_shaped(start_date, end_date)
            coils[i].calculated_quantity_stock = coils[i].quantity_stock()
            coils[i].calculated_weight_stock = coils[i].weight_stock()

        machines = Machine.objects.all()
        for i in range(machines.__len__()):
            machines[i].calculated_extrusion_number = machines[i].extrusion_number(start_date, end_date)
            machines[i].calculated_extrusion_weight = machines[i].extrusion_weight(start_date, end_date)

            machines[i].calculated_printing_number = machines[i].printing_number(start_date, end_date)
            machines[i].calculated_printing_weight = machines[i].printing_weight(start_date, end_date)

            machines[i].calculated_shaping_number = machines[i].shaping_number(start_date, end_date)
            machines[i].calculated_shaping_weight = machines[i].shaping_weight(start_date, end_date)

            machines[i].calculated_production_number = machines[i].production_number(start_date, end_date)
            machines[i].calculated_production_weight = machines[i].production_weight(start_date, end_date)

            machines[i].calculated_trash_weight = machines[i].trash_weight(start_date, end_date)
        

        users = Profile.objects.filter(Q(job_position__name ="Mélangeur") | Q(job_position__name ="Opérateur Extrusion") | Q(job_position__name ="Opérateur Façonnage"))
        for i in range(users.__len__()):
            users[i].calculated_extrusion_number = users[i].extrusion_number(start_date, end_date)
            users[i].calculated_extrusion_weight = users[i].extrusion_weight(start_date, end_date)

            users[i].calculated_printing_number = users[i].printing_number(start_date, end_date)
            users[i].calculated_printing_weight = users[i].printing_weight(start_date, end_date)

            users[i].calculated_shaping_number = users[i].shaping_number(start_date, end_date)
            users[i].calculated_shaping_weight = users[i].shaping_weight(start_date, end_date)

            
        
        suppliers = Contact.objects.filter(contact_type="SUPPLIER")
        for i in range(suppliers.__len__()):
            suppliers[i].calculated_extrusion_number = suppliers[i].extrusion_number(start_date, end_date)
            suppliers[i].calculated_extrusion_weight = suppliers[i].extrusion_weight(start_date, end_date)

            suppliers[i].calculated_defective_number = suppliers[i].defective_number(start_date, end_date)
            suppliers[i].calculated_defective_weight = suppliers[i].defective_weight(start_date, end_date)

            suppliers[i].calculated_quarantine_number = suppliers[i].quarantine_number(start_date, end_date)
            suppliers[i].calculated_quarantine_weight = suppliers[i].quarantine_weight(start_date, end_date)

            suppliers[i].calculated_destroy_number = suppliers[i].destroy_number(start_date, end_date)
            suppliers[i].calculated_destroy_weight = suppliers[i].destroy_weight(start_date, end_date)


        clients = Contact.objects.filter(contact_type = "CLIENT")
        for i in range(clients.__len__()):
            clients[i].calculated_number_sold = clients[i].number_sold(start_date, end_date)
            clients[i].calculated_weight_sold = clients[i].weight_sold(start_date, end_date)
        
        parts = SparePart.objects.all()
        for i in range(parts.__len__()):
            parts[i].calculated_quantity_consumed = parts[i].quantity_consumed(start_date, end_date)
            parts[i].calculated_quantity_brought = parts[i].quantity_brought(start_date, end_date)

        defective_coils = Coil.objects.filter(Q(creation_date__gte = start_date) & Q(creation_date__lte = end_date) & Q(defective = "DEFECTIVE"))
        quarantine_coils = Coil.objects.filter(Q(creation_date__gte = start_date) & Q(creation_date__lte = end_date) & Q(status = "QUARANTINE"))
        destroy_coils = Coil.objects.filter(Q(creation_date__gte = start_date) & Q(creation_date__lte = end_date) & Q(status = "TO_BE_DESTROYED"))
        
        defective_coils_number_total = 0
        quarantine_coils_number_total = 0
        destroy_coils_number_total = 0
        defective_coils_weight_total = 0
        quarantine_coils_weight_total = 0
        destroy_coils_weight_total = 0

        defective_coils_number_total = defective_coils.count()
        quarantine_coils_number_total = quarantine_coils.count()
        destroy_coils_number_total = destroy_coils.count()

        for c in defective_coils.all():
            defective_coils_weight_total += c.weight

        for c in quarantine_coils.all():
            quarantine_coils_weight_total += c.weight
        
        for c in destroy_coils.all():
            destroy_coils_weight_total += c.weight

        printed_coils = Coil.objects.exclude(status = "CUT").filter(Q(creation_date__gte = start_date) & Q(creation_date__lte = end_date) & Q(printed = "PRINTED"))
        not_printed_coils = Coil.objects.exclude(status = "CUT").filter(Q(creation_date__gte = start_date) & Q(creation_date__lte = end_date) & Q(printed = "NOT_PRINTED"))

        printed_coils_number = 0
        printed_coils_weight = 0
        printed_coils_number = printed_coils.count()
        for c in printed_coils:
            printed_coils_weight += c.weight
        
        not_printed_coils_number = 0
        not_printed_coils_weight = 0
        not_printed_coils_number = not_printed_coils.count()
        for c in not_printed_coils:
            not_printed_coils_weight += c.weight
        
        if printed_coils_number + not_printed_coils_number != 0:
            not_printed_coils_pourcentage = not_printed_coils_number/(printed_coils_number + not_printed_coils_number)*100
            printed_coils_pourcentage = 100 - not_printed_coils_pourcentage
        else:
            not_printed_coils_pourcentage = 0
            printed_coils_pourcentage = 0
        
        coils_number = 0
        coils_weight = 0

        coils_number = printed_coils_number + not_printed_coils_number
        coils_weight = printed_coils_weight + not_printed_coils_weight
            
        

        trash = Trash.objects.filter(Q(state = "VALIDATED") & Q(date__gte = start_date) & Q(date__lte = end_date))

        trash_high = trash.filter(trash_type="HAUTE_DENSITE")
        trash_high_weight = 0
        for t in trash_high:
            if t.weight is not None:
                trash_high_weight += t.weight
            else:
                trash_high_weight += t.weight
        
        trash_low = trash.filter(trash_type="BASSE_DENSITE")
        trash_low_weight = 0
        for t in trash_low:
            if t.weight is not None:
                trash_low_weight += t.weight
            else:
                trash_low_weight += t.weight
        
        total_trash = trash_high_weight + trash_low_weight

        template = loader.get_template('production/reporting.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "users": users,
            "clients": clients,
            "suppliers": suppliers,
            "raw_matters":raw_matters,
            "products":products,
            "packages":packages,
            "labellings":labellings,
            "handles":handles,
            "coils":coils,
            "product_combined_ranges":product_combined_ranges,
            "matter_combined_ranges":matter_combined_ranges,
            "black_production":black_production,
            "color_production":color_production,
            "black_production_pourcentage":black_production_pourcentage,
            "color_production_pourcentage":color_production_pourcentage,
            "black_sales":black_sales,
            "color_sales":color_sales,
            "black_sales_pourcentage":black_sales_pourcentage,
            "color_sales_pourcentage":color_sales_pourcentage,
            "total_sales":total_sales,
            "total_production":total_production,
            "printed_coils_number":printed_coils_number,
            "printed_coils_weight":printed_coils_weight,
            "not_printed_coils_number":not_printed_coils_number,
            "not_printed_coils_weight":not_printed_coils_weight,
            "printed_coils_pourcentage":printed_coils_pourcentage,
            "not_printed_coils_pourcentage":not_printed_coils_pourcentage,
            "coils_number":coils_number,
            "coils_weight":coils_weight,
            "defective_coils_number_total":defective_coils_number_total ,
            "defective_coils_weight_total":defective_coils_weight_total,
            "quarantine_coils_number_total":quarantine_coils_number_total,
            "quarantine_coils_weight_total":quarantine_coils_weight_total,
            "destroy_coils_number_total":destroy_coils_number_total,
            "destroy_coils_weight_total":destroy_coils_weight_total,
            "trash_high_weight":trash_high_weight,
            "trash_low_weight":trash_low_weight,
            "total_trash":total_trash,
            "machines":machines,
            "parts":parts,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('production/reporting.html', context)
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

def mini_reporting(request):
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

        mixings = Order.objects.exclude(machine=None).all()
        mixings = mixings.filter(ordered_date__gte = start_date)
        mixings = mixings.filter(ordered_date__lte = end_date)

        total_mixing_weight = 0
        total_mixing_amount = 0
        for i in mixings:
            total_mixing_weight += i.get_total()
            total_mixing_amount += i.get_amount()

        coils = CoilType.objects.all()
        for i in range(coils.__len__()):
            coils[i].calculated_quantity_produced = coils[i].quantity_produced(start_date, end_date)
            coils[i].calculated_weight_produced = coils[i].weight_produced(start_date, end_date)
            coils[i].calculated_amount_produced = coils[i].amount_produced(start_date, end_date)
        
        coilss = Coil.objects.all()
        coilss = coilss.filter(creation_date__gte = start_date)
        coilss = coilss.filter(creation_date__lte = end_date)
        total_coil_weight = 0
        total_amount_produced = 0
        total_coil_number = coilss.count()
        for i in coilss:
            total_amount_produced += i.weight * Decimal(i.type_coil.price)
            total_coil_weight += i.weight

        products = FinishedProductType.objects.all()
        for i in range(products.__len__()):
            products[i].calculated_quantity_produced = products[i].quantity_produced(start_date, end_date)
            products[i].calculated_weight_produced = products[i].weight_produced(start_date, end_date)
            products[i].calculated_amount_produced = products[i].amount_produced(start_date, end_date)

        productions = Production.objects.filter(process_type = "FINISHED_PRODUCT")
        productions = productions.filter(date__gte = start_date)
        productions = productions.filter(date__lte = end_date)

        total_product_number = 0
        total_product_weight = 0
        total_product_amount = 0
        for p in productions:
            total_product_number += p.quantity_produced
            total_product_weight += p.weight
            total_product_amount += p.quantity_produced * Decimal(p.product.price) * Decimal(p.product.roll_package)

        trashes = Trash.objects.all()
        trashes = trashes.filter(date__gte = start_date)
        trashes = trashes.filter(date__lte = end_date)

        total_trash = 0
        for t in trashes:
            total_trash += t.weight

        template = loader.get_template('production/mini_reporting.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "mixings": mixings,
            "total_mixing_weight":total_mixing_weight,
            "total_mixing_amount":total_mixing_amount,
            "total_coil_weight":total_coil_weight,
            "total_coil_number":total_coil_number,
            "total_amount_produced":total_amount_produced,
            "total_product_number":total_product_number,
            "total_product_weight":total_product_weight,
            "total_product_amount":total_product_amount,
            "total_trash":total_trash,
            "coils":coils,
            "products":products,
            "trashes":trashes,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('production/mini_reporting.html', context)
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

class PointPage(View):
    template_name = 'production/point_page.html'

    def get(self, request):
        return render(request, "production/point_page.html", context={"job_positions": JobPosition.objects.exclude(name="Administrateur").exclude(name="Gérant").all()})

class GeneralSalaryPage(View):
    template_name = 'production/general_salary_page.html'

    def get(self, request):
        return render(request, "production/general_salary_page.html")

class GlobalPointPage(View):
    template_name = 'production/global_point_page.html'

    def get(self, request):
        return render(request, "production/global_point_page.html")

class PointView(View):
    model = Point
    template_name = 'profile/point_create.html'
    success_url = reverse_lazy('production:index-personnel')

    def get(self, request, *arg, **kwargs):
        form = PointForm()
        users = User.objects.filter(profile__group = request.user.profile.group)
        context = {
            'users':users,
            'form': form,
        }
        return render(self.request, 'profile/point_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PointForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                start_hour = Decimal(request.POST.get("start_hour"))
                start_minute = Decimal(request.POST.get("start_minute"))
                end_hour = Decimal(request.POST.get("end_hour"))
                end_minute = Decimal(request.POST.get("end_minute"))

                start_date = form.start_date
                end_date = form.end_date
                # transport = form.transport
                absence = form.absence
                holiday = form.holiday
                # if transport is None : transport = 0
                if absence is None : absence = 0

                try:
                    user_id = request.POST.get("user")
                    user = User.objects.get(username= user_id)
                except:
                    messages.error(request, "Utilisateur Introuvable")
                    return redirect(request.META.get('HTTP_REFERER'))
                start_date = start_date.replace(hour = start_hour, minute = start_minute, second = 0, microsecond = 0)
                end_date = end_date.replace(hour = end_hour, minute = end_minute, second = 0, microsecond = 0)
                
                for i in Point.objects.filter(user = user):
                    if start_date.day == i.start_date.day and start_date.month == i.start_date.month and start_date.year == i.start_date.year:
                        messages.error(request, "Pointage Existant")
                        return redirect(request.META.get('HTTP_REFERER'))

                duration = end_date - start_date
                duration = duration.total_seconds()/60 - float(absence)*60

                hours = duration // 60

                minutes = duration % 60

                if duration < 0:
                    messages.error(request, "Dates érronées")
                    return redirect(request.META.get('HTTP_REFERER'))

                if absence*60 == duration:
                    point = Point(date = timezone.now(),user = user, start_date = start_date, end_date = end_date, duration = duration, hours = hours, minutes = minutes, absence = absence, is_absent = True, holiday = holiday, valid = False)
                else:
                    point = Point(date = timezone.now(),user = user, start_date = start_date, end_date = end_date, duration = duration, hours = hours, minutes = minutes, absence = absence, is_absent= False, holiday = holiday, valid = False)
                
                point.save()

                return redirect(self.success_url)

class CoilUpdateView(UpdateView):
    template_name = 'production/update_coil.html'
    form_class = CoilForm
    success_url = reverse_lazy('production:coil-consulting')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour une Bobine'
        return context

    def get_object(self):
        _ref = self.kwargs.get('ref')
        return get_object_or_404(Coil, ref=_ref)

class ProductionUpdateView(UpdateView):
    template_name = 'production/update_production.html'
    form_class = ProductionForm
    success_url = reverse_lazy('production:finished-product-consulting')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour une Production'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Production, slug=_slug)

def delete_coil(request, ref):
    coil = get_object_or_404(Coil, ref=ref)
    try:
        extrusion = Production.objects.get(process_type="EXTRUSION", coil = coil)
        extrusion.delete()
    except:
        pass
    
    try:
        printing = Production.objects.get(process_type="PRINTING", coil = coil)
        printing.delete()
    except:
        pass

    try:
        shaping = Production.objects.get(process_type="SHAPING", coil = coil)
        shaping.delete()
    except:
        pass

    try:
        sale = CoilSale.objects.get( coil = coil)
        sale.delete()
    except:
        pass
    
    if coil.status == "PENDING_EXTRUSION":
        coil.extrusion_machine.state = "FREE"
        coil.extrusion_machine.save()
    elif coil.status == "PENDING PRINTING":
        coil.printing_machine.state = "FREE"
        coil.printing_machine.save()
    elif coil.status == "PENDING_SHAPING":
        coil.shaping_machine.state = "FREE"
        coil.shaping_machine.save()

    coil.delete()

    return redirect(reverse_lazy("production:coil-consulting"))


def points(request):
    current_time = None
    if request.method == "GET":
        
        holiday_salary = 0
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        user_first = request.GET.get("user-first")
        user_last = request.GET.get("user-last")
        user_job = request.GET.get("user-job")
        # holiday_salary = Decimal(request.GET.get("holiday-salary"))
        imposed_bonus = Decimal(request.GET.get("bonus"))
        start_date = parse_date(from_date)
        end_date = parse_date(to_date)
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = start_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        end_date = end_date.replace(hour = 23, minute = 59, second = 59, microsecond = 0)
        try:
            user = User.objects.get(first_name__icontains = user_first, last_name__icontains = user_last, profile__job_position__slug = user_job)
        except:
            messages.error(request, "Aucun employé trouvé, veuillez vérifier le nom")
            return redirect(request.META.get('HTTP_REFERER'))
        
        company = Company.objects.filter(name ="Ln Plast")[0]
        ####################### Pointage #######################
        points = Point.objects.filter(user = user)
        points = points.filter(start_date__gte = start_date)
        points = points.filter(start_date__lte = end_date)

        presence = points.exclude(holiday = True).filter(is_absent = False)
        holidays = points.filter(is_absent = False, holiday = True)

        if user.profile.job_position.name == "Opérateur Extrusion" or user.profile.job_position.name == "Opérateur Façonnage" or user.profile.job_position.name == "Gestionnaire de Stock":
            holiday_salary = Decimal(((36000/176)*8)*holidays.count())
        else:
            holiday_salary = Decimal(((30000/176)*8)*holidays.count())

        points_total = 0
        quality = 0
        quantity = 0
        motivation = 0
        attitude = 0
        punctuality = 0
        look = 0
        penalty = 0
        prime = 0
        transport_total = 0
        quality_mean = 0
        quantity_mean = 0
        motivation_mean = 0
        attitude_mean = 0
        punctuality_mean = 0
        look_mean = 0

        for j in points:
            if j.penality is not None:
                penalty += j.penality
            if j.prime is not None:
                prime += j.prime

        for point in presence:
            quality += point.quality
            quantity += point.quantity
            motivation += point.motivation
            attitude += point.attitude
            punctuality += point.punctuality
            look += point.look
            if point.user.last_name == "Bourahla" and point.user.first_name == "Abdelkader":
                transport_total += 1590
            if point.user.profile.self_transported is True:
                transport_total += 300
            points_total += point.duration
        try:
            quality_mean = quality / presence.count()
        except:
            pass
        try:
            quantity_mean = quantity / presence.count()
        except:
            pass
        try:
            motivation_mean = motivation / presence.count()
        except:
            pass
        try:
            attitude_mean = attitude / presence.count()
        except:
            pass
        try:
            punctuality_mean = punctuality / presence.count()
        except:
            pass
        try:
            look_mean = look / presence.count()
        except:
            pass

        hiring_date = user.profile.hiring_date

        now = timezone.now()
        
        years = now.year - hiring_date.year
        if now.month - hiring_date.month < 0:
            years = years -1

        user_base_salary = user.profile.salary

        if imposed_bonus == 100:
            mean_sum = quality_mean + quantity_mean + motivation_mean + attitude_mean + punctuality_mean + look_mean
        else:
            mean_sum = imposed_bonus
        
        if points_total - 10560 >= 0 :
            additional_time = points_total - 10560
        else:
            user_base_salary = (user_base_salary / 176 ) * (points_total//60)
            additional_time = 0
        additional_time_h = additional_time // 60
        additional_time_m = additional_time % 60


        iep = ((user_base_salary * 1)/100) * years
        cotisable = user_base_salary + iep
        ss = (cotisable * 9)/100 * (-1)


        if (points_total//60)%8 == 0:
            trans = ((points_total//60)/8) * 250
        else:
            trans = (((points_total//60)//8)+1) * 250

        if trans > 5500:
            trans = 5500


        if (points_total//60)%8 == 0:
            panier = ((points_total//60)/8) * 300
        else:
            panier = (((points_total//60)//8)+1) * 300
        if panier > 6600:
            panier = 6600
        
        imposable = Decimal(cotisable) + Decimal(panier) + Decimal(trans) + Decimal(ss)

        if imposable % 10 == 0:
            round_imposable = imposable
        else:
            round_imposable = imposable - (imposable%10)

        irg = 0
        if imposable >= 35000:
            irg = -(((round_imposable - 35000)/10)*3 + 4000)
        elif imposable >= 30000 and imposable < 35000:
            irg = -(((round_imposable - 30000)/10)*8)
        else:
            irg = 0

        net = imposable + irg
        
        salary = 0
        user_bonus_pourcentage = user.profile.bonus
        bonus = ((((net * user_bonus_pourcentage) /100) * mean_sum)/100) + ((imposable /10560)*2 * additional_time) + transport_total + prime - penalty
        
        salary = net + bonus + holiday_salary
        found = False
        for sal in Salary.objects.filter(user = user):
            ds = sal.start_date
            de = sal.end_date
            if ds.day == start_date.day and ds.month == start_date.month and ds.year == start_date.year and de.day == end_date.day and de.month == end_date.month and de.year == end_date.year:
                found = True
        if found == False:
            slr = Salary(user = user, date = timezone.now(), start_date = start_date, end_date = end_date, base_salary = user_base_salary, salary = salary, iep = iep, cotisable = cotisable ,ss = ss, panier = panier, trans= trans, imposable = imposable, net = net, irg = irg, bonus = bonus ,holiday = holiday_salary, valid = False)
            slr.save()
        pt = points_total // 60
        min_pt = points_total % 60
        template = loader.get_template('production/pointage.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "user": user,
            "points": points,
            "points_total": points_total,
            "pt": pt,
            "min_pt":min_pt,
            "mean_sum":mean_sum,
            "additional_time_h": additional_time_h,
            "additional_time_m": additional_time_m,
            "holiday_salary": holiday_salary,
            "salary": salary,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('production/pointage.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Pointage %s %s - %s.pdf" % (user, start_date, end_date)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def general_salaries(request):
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
        
        users = User.objects.filter(profile__active = True)
        
        ####################### Pointage #######################

        for user in users:
            points = Point.objects.filter(user = user)
            points = points.filter(start_date__gte = start_date)
            points = points.filter(start_date__lte = end_date)

            presence = points.exclude(holiday = True).filter(is_absent = False)
            holidays = points.filter(is_absent = False, holiday = True)

            holiday_salary = 0

            if user.profile.job_position.name == "Opérateur Extrusion" or user.profile.job_position.name == "Opérateur Façonnage" or user.profile.job_position.name == "Gestionnaire de Stock":
                holiday_salary = Decimal(((36000/176)*8)*holidays.count())
            else:
                holiday_salary = Decimal(((30000/176)*8)*holidays.count())

            points_total = 0
            quality = 0
            quantity = 0
            motivation = 0
            attitude = 0
            punctuality = 0
            look = 0
            penalty = 0
            prime = 0
            transport_total = 0

            for j in points:
                if j.penality is not None:
                    penalty += j.penality
                if j.prime is not None:
                    prime += j.prime

            for point in presence:
                quality += point.quality
                quantity += point.quantity
                motivation += point.motivation
                attitude += point.attitude
                punctuality += point.punctuality
                look += point.look
                if point.user.last_name == "Bourahla" and point.user.first_name == "Abdelkader":
                    transport_total += 1590
                if point.user.profile.self_transported is True:
                    transport_total += 300
                points_total += point.duration
            try:
                quality_mean = quality / presence.count()
            except:
                pass
            try:
                quantity_mean = quantity / presence.count()
            except:
                pass
            try:
                motivation_mean = motivation / presence.count()
            except:
                pass
            try:
                attitude_mean = attitude / presence.count()
            except:
                pass
            try:
                punctuality_mean = punctuality / presence.count()
            except:
                pass
            try:
                look_mean = look / presence.count()
            except:
                pass

            hiring_date = user.profile.hiring_date

            now = timezone.now()

            years = now.year - hiring_date.year
            if now.month - hiring_date.month < 0:
                years = years -1

            user_base_salary = user.profile.salary

            mean_sum = quality_mean + quantity_mean + motivation_mean + attitude_mean + punctuality_mean + look_mean

            if points_total - 10560 >= 0 :
                additional_time = points_total - 10560
            else:
                user_base_salary = (user_base_salary / 176 ) * (points_total//60)
                additional_time = 0
            additional_time_h = additional_time // 60
            additional_time_m = additional_time % 60


            iep = ((user_base_salary * 1)/100) * years
            cotisable = user_base_salary + iep
            ss = (cotisable * 9)/100 * (-1)


            if (points_total//60)%8 == 0:
                trans = ((points_total//60)/8) * 250
            else:
                trans = (((points_total//60)//8)+1) * 250

            if trans > 5500:
                trans = 5500


            if (points_total//60)%8 == 0:
                panier = ((points_total//60)/8) * 300
            else:
                panier = (((points_total//60)//8)+1) * 300
            if panier > 6600:
                panier = 6600

            imposable = cotisable + panier + trans + ss

            if imposable % 10 == 0:
                round_imposable = imposable
            else:
                round_imposable = imposable - (imposable%10)

            irg = 0
            if imposable >= 35000:
                irg = -(((round_imposable - 35000)/10)*3 + 4000)
            elif imposable >= 30000 and imposable < 35000:
                irg = -(((round_imposable - 30000)/10)*8)
            else:
                irg = 0

            net = imposable + irg

            salary = 0
            user_bonus_pourcentage = user.profile.bonus
            bonus = ((((net * user_bonus_pourcentage) /100) * mean_sum)/100) + ((imposable /10560)*2 * additional_time) + transport_total + prime - penalty

            salary = net + bonus + holiday_salary
            found = False
            for sal in Salary.objects.filter(user = user):
                ds = sal.start_date
                de = sal.end_date
                if ds.day == start_date.day and ds.month == start_date.month and ds.year == start_date.year and de.day == end_date.day and de.month == end_date.month and de.year == end_date.year:
                    found = True
            if found is False:
                slr = Salary(user = user, date = timezone.now(), start_date = start_date, end_date = end_date, base_salary = user_base_salary, salary = salary, iep = iep, cotisable = cotisable ,ss = ss, panier = panier, trans= trans, imposable = imposable, net = net, irg = irg, bonus = bonus ,holiday = holiday_salary, valid = False)
                slr.save()
        return redirect(reverse_lazy("production:salaries"))
        



def global_points(request):
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

        users = Profile.objects.filter(active = True)
        points = Point.objects.all()
        points = points.filter(start_date__gte = start_date)
        points = points.filter(start_date__lte = end_date)

        for i in range(users.__len__()):
            users[i].calculated_presence_time = users[i].presence_time(start_date, end_date)
            users[i].calculated_absence_time = users[i].absence_time(start_date, end_date)
        company = Company.objects.filter(name ="Ln Plast")[0]
        template = loader.get_template('production/global_points.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "users": users,
            "points": points,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('production/global_points.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Pointage Globale%s.pdf" % (timezone.now())
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def print_salaries(request):
    company = Company.objects.filter(name ="Ln Plast")[0]
    salaries = Salary.objects.filter(valid = False)
    total_salaries = 0
    for salary in salaries:
        total_salaries += salary.salary
    template = loader.get_template('production/print_salaries.html')
    context = {
        "salaries":salaries,
        "total_salaries":total_salaries,
        "company": company,
    }
    html = template.render(context)
    pdf = render_to_pdf('production/print_salaries.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "salaries%s.pdf" % (timezone.now())
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def my_points(request):
    now = timezone.now()
    now = now.replace(day = 1, hour = 1, minute = 0, second = 0)

    points = Point.objects.filter(start_date__gte= now ,user__profile__group=request.user.profile.group)
    return render(request, 'profile/list/my_points_list.html', context={'object_list': points, 'users': User.objects.filter(profile__group = request.user.profile.group, profile__active = True)})

def delete_point(request, slug):
    point = get_object_or_404(Point, slug=slug)
    point.delete()

    if request.user.profile.job_position.name == "Administrateur":
        queryset = Point.objects.filter(valid=False)
        return render(request, 'production/pending_points.html', context={'object_list': queryset})
    else:
        return redirect(reverse_lazy("production:my-points"))

def validate_point(request):
    
    if request.method == "POST":
        point_slug = request.POST.get("get_point")
        point = get_object_or_404(Point, slug=point_slug)

        quality = Decimal(request.POST.get("quality"))
        quantity = Decimal(request.POST.get("quantity"))
        motivation = Decimal(request.POST.get("motivation"))
        attitude = Decimal(request.POST.get("attitude"))
        punctuality = Decimal(request.POST.get("punctuality"))
        look = Decimal(request.POST.get("look"))
        penality = Decimal(request.POST.get("penality"))
        prime = Decimal(request.POST.get("prime"))
        holiday = request.POST.get("holiday")
        is_on_holiday = request.POST.get("break")

        point.quality = quality
        point.quantity = quantity
        point.motivation = motivation
        point.attitude = attitude
        point.punctuality = punctuality
        point.look = look
        point.penality = penality
        point.prime = prime
        if holiday == 'on':
            point.duration = point.duration * 2
            if point.minutes * 2 >= 60:
                point.minutes = (point.minutes * 2) - 60
                point.hours = (point.hours * 2) +1
            elif point.minutes * 2 < 60:
                point.minutes = point.minutes * 2
                point.hours = point.hours * 2
        
        if is_on_holiday == 'on':
            point.holiday = True

        point.valid = True
        point.save()

        # if point.absence != 0:    
        #     email(request, f'Notification TayPlast : Absence {point.user.first_name.upper()} {point.user.last_name.upper()}', f"Bonjour,\n L'employé {point.user.first_name.upper()} {point.user.last_name.upper()} a été absent le {point.start_date:%d-%m-%Y}. \n\n\n\t S.A.R.L TayPlast", 'mounir.benhalima@tayplast-dz.com', None, None, None, None, None)
        # return redirect(reverse_lazy("production:validate-point"))
    now = timezone.now()
    month = now.month -1
    now = now.replace(day = 25, month = month, hour= 0, minute= 0)
    queryset = Point.objects.filter(valid=False)
    return render(request, 'production/pending_points.html', context={'object_list': queryset})

class SalariesView(ListView):

    template_name = 'production/salaries.html'

    def get_queryset(self, **kwargs):
        now = timezone.now()
        month = now.month - 1
        now = now.replace(day = 1, month=month, hour = 0)
        queryset = Salary.objects.filter(date__gte = now)
        return queryset

def delete_salary(request, slug):
    salary = get_object_or_404(Salary, slug=slug)
    salary.delete()
    return redirect(reverse_lazy("production:salaries"))

def delete_salaries(request):
    salaries = Salary.objects.filter(valid=False)
    for salary in salaries:
        salary.delete()
    return redirect(reverse_lazy("production:salaries"))

def validate_salaries(request):
    salaries = Salary.objects.filter(valid=False)
    for salary in salaries:
        salary.valid = True
        salary.save()
    return redirect(reverse_lazy("production:salaries"))

def validate_holiday_request(request, slug):
    holiday_request = get_object_or_404(HolidayRequest, slug=slug)
    if request.user.profile.job_position.name == "Administrateur":
        holiday_request.state = "ACCEPTED"
        holiday_request.validation_date = timezone.now()
        holiday_request.validator = request.user
        holiday_request.save()
        return redirect(reverse_lazy("production:holiday-request-list"))
        user = holiday_request.user
        start_date = holiday_request.start_date
        end_date = holiday_request.end_date
        company = Company.objects.filter(name ="Ln Plast")[0]
        template = loader.get_template('production/holiday_report.html')
        context = {
            "start_date": start_date,
            "end_date": end_date,
            "user": user,
            "holiday":holiday_request,
            "company": company,
        }
        html = template.render(context)
        pdf = render_to_pdf('production/holiday_report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Demande de congé %s.pdf" % (user)
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def print_holiday_request(request, slug):
    holiday_request = get_object_or_404(HolidayRequest, slug=slug)
    user = holiday_request.user
    start_date = holiday_request.start_date
    end_date = holiday_request.end_date
    validation_date = holiday_request.validation_date
    validator = holiday_request.validator
    current_user = request.user
    company = Company.objects.filter(name ="Ln Plast")[0]
    template = loader.get_template('production/holiday_report.html')
    context = {
        "start_date": start_date,
        "end_date": end_date,
        "user": user,
        "holiday":holiday_request,
        "validation_date":validation_date,
        "validator":validator,
        "company": company,
    }
    html = template.render(context)
    pdf = render_to_pdf('production/holiday_report.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Demande de congé %s.pdf" % (user)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
    
def reject_holiday_request(request, slug):
    holiday_request = get_object_or_404(HolidayRequest, slug=slug)
    if request.user.profile.job_position.name == "Administrateur":
        holiday_request.state = "REJECTED"
        holiday_request.save()
        return redirect(reverse_lazy("production:holiday-request-list"))


def delete_holiday_request(request, slug):
    holiday_request = get_object_or_404(HolidayRequest, slug=slug)
    holiday_request.delete()
    if request.user.profile.job_position.name == "Administrateur":
        return redirect(reverse_lazy("production:holiday-request-list"))
    else:
        return redirect(reverse_lazy("production:my-holidays"))


def employee(request, slug):
    user = get_object_or_404(Profile, slug = slug)
    company = Company.objects.filter(name ="Ln Plast")[0]

    if user.job_position.name == "Opérateur Extrusion":
        coils =  Coil.objects.filter(user=user.user)
    elif user.job_position.name == "Opérateur Impression":
        coils =  Coil.objects.filter(printer=user.user)
    elif user.job_position.name == "Opérateur Façonnage":
        coils =  Coil.objects.filter(maker=user.user)
    
    coils_total_weight = 0

    for coil in coils:
        if coil.weight is not None:
            coils_total_weight += coil.weight

    template = loader.get_template('production/employee.html')
    context = {
        "user": user,
        "company": company,
        "coils_total_weight":coils_total_weight,
    }

    html = template.render(context)
    pdf = render_to_pdf('production/employee.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "employee%s.pdf" % (timezone.now())
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


class ExtrusionCreateView(View):
    model = Production
    template_name = 'production/extrusion.html'
    success_url = reverse_lazy('production:extrusion-coil-list')

    def get(self, request, *arg, **kwargs):
        form = ExtrusionForm()
        context = {
            'form': form,
            'ranges':Range.objects.all(),
            'colors':Color.objects.all(),
            'flavors':Flavor.objects.all(),
        }
        return render(self.request, 'production/extrusion.html', context)

    def post(self, request, *args, **kwargs):
        form = ExtrusionForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                
                # coil_range = request.POST.get("range")
                # coil_capacity = request.POST.get("capacity")
                # try:
                #     coil_capacity = int(coil_capacity)
                # except:
                #     messages.error(request, "Veuillez choisir la capacité")
                #     return redirect(request.META.get('HTTP_REFERER'))
                # coil_color = request.POST.get("color")
                # coil_link = request.POST.get("link")
                # coil_perfume = request.POST.get("perfume")
                # coil_flavor = request.POST.get("flavor")
                # if coil_flavor == "None" : coil_flavor = None

                # print(coil_range, "-",coil_capacity, "-", coil_color, "-", coil_link, "-", coil_perfume, "-", coil_flavor)
                # try:
                #     product_confirmation = CoilType.objects.get(name__slug = coil_range, capacity = coil_capacity, color__name = coil_color, link = coil_link, perfume = coil_perfume, flavor__name = coil_flavor )
                # except:
                #     messages.error(request, "Bobine Introuvable")
                #     return redirect(request.META.get('HTTP_REFERER'))

                product = form.coil_type

                # if product != product_confirmation:
                #     messages.error(request, "Bobines Incohérentes")
                #     return redirect(request.META.get('HTTP_REFERER'))

                machine = form.machine
                user = self.request.user

                extrusion = Production(date=timezone.now(),coil_type = product, user=request.user, quantity_produced=1, machine=machine, process_type="EXTRUSION", state="PENDING")
                ref = get_random_string(15)
                
                coil = Coil(user=user, type_coil = product , extrusion_machine = extrusion.machine, ref=ref, creation_date=timezone.now(), name=product.name, quantity=1, type_name=product.type_name, capacity=product.capacity,
                                perfume=product.perfume, brand=product.brand, color=product.color, warehouse=product.warehouse, printed="NOT_PRINTED")
                coil.save()
                extrusion.coil = coil
                mchn = Machine.objects.get(slug=machine.slug)
                mchn.state = "OCCUPIED"
                mchn.save()
                extrusion.save()
                return redirect(self.success_url)

class MachineStopCreateView(View):
    model = MachineStop
    template_name = 'production/machine_stop.html'

    def get(self, request, *arg, **kwargs):
        if request.user.profile.job_position.name == "Opérateur Extrusion":
            form = ExtrusionMachineStopForm()
        elif request.user.profile.job_position.name == "Opérateur Impression":
            form = PrintingMachineStopForm()
        elif request.user.profile.job_position.name == "Opérateur Façonnage":
            form = ShapingMachineStopForm()
        elif request.user.profile.job_position.name == "Mélangeur":
            form = MixingMachineStopForm()
        context = {
            'form': form,
        }
        return render(self.request, 'production/machine_stop.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.profile.job_position.name == "Opérateur Extrusion":
            form = ExtrusionMachineStopForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Impression":
            form = PrintingMachineStopForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Façonnage":
            form = ShapingMachineStopForm(request.POST)
        elif request.user.profile.job_position.name == "Mélangeur":
            form = MixingMachineStopForm(request.POST)

        if self.request.method == "POST":
            
            if form.is_valid():
                form = form.save(commit=False)
                user = self.request.user
                machine = form.machine
                hours = form.hours
                minutes = form.minutes
                cause = form.cause
                comment = form.comment
                machine_stop = MachineStop(date = timezone.now(), user = user, machine= machine, hours = hours, minutes = minutes, cause = cause, comment=comment)
                machine_stop.save()
                if request.user.profile.job_position.name == "Opérateur Extrusion":
                    return redirect(reverse_lazy('production:index-extrusion'))
                elif request.user.profile.job_position.name == "Opérateur Impression":
                    return redirect(reverse_lazy('production:index-printing'))
                elif request.user.profile.job_position.name == "Opérateur Façonnage":
                    return redirect(reverse_lazy('production:index-shaping'))
                if request.user.profile.job_position.name == "Mélangeur":
                    return redirect(reverse_lazy('production:index-mixing'))
                

def extrusion_coil_list(request):
    weight = None
    micronnage = None
    coil = None
    consumed = None
    mandrel_weight = None
    if request.method == "POST":
        weight = Decimal(request.POST.get("weight"))
        micronnage = request.POST.get("micronnage")
        mandrel_weight = Decimal(request.POST.get("mandrel_weight"))
        
        coil_slug = request.POST.get("get_coil")
        coil = get_object_or_404(Coil, slug=coil_slug)
        extrusion = Production.objects.get(process_type="EXTRUSION", coil=coil)
        extrusion.state = "FINISHED"
        machine = coil.extrusion_machine
        machine.state = "FREE"
        machine.save()
        coil.weight = weight - mandrel_weight
        coil.micronnage = micronnage
        coil.status = "IN_STOCK"
        coil.introducer = request.user
        extrusion.save()
        coil.save()
    return render(request, 'production/extrusion_coil_list.html', context={'object_list': Coil.objects.filter(status="PENDING_EXTRUSION") | Coil.objects.filter(user=request.user, ticket_printed = False) | Coil.objects.filter(introducer=request.user, ticket_printed = False)})

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Créer Bobine'
        return context

def print_ticket(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    coil.ticket_printed = True
    coil.save()
    template = loader.get_template('production/coil_ticket.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "coil": coil,

    }
    html = template.render(context)
    pdf = render_to_pdf('production/coil_ticket.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" % (coil.product_designation)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def print_issue_ticket(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    template = loader.get_template('production/coil_issue_ticket.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "coil": coil,

    }
    html = template.render(context)
    pdf = render_to_pdf('production/coil_issue_ticket.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "{coil.get_status_display}-{coil.product_designation}%s.pdf" % ("12341231")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def print_ticket_no_qr(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    coil.ticket_printed = True
    coil.save()
    template = loader.get_template('production/coil_ticket_no_qr.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "coil": coil,

    }
    html = template.render(context)
    pdf = render_to_pdf('production/coil_ticket_no_qr.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s.pdf" % (coil.product_designation)
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def print_issue_ticket_no_qr(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    template = loader.get_template('production/coil_issue_ticket_no_qr.html')
    try:
        company = Company.objects.filter(name='Ln Plast')[0]
    except:
        company = 'Ln Plast'
    context = {
        "user": request.user,
        "company": company,
        "coil": coil,

    }
    html = template.render(context)
    pdf = render_to_pdf('production/coil_issue_ticket_no_qr.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "{coil.get_status_display}-{coil.product_designation}%s.pdf" % ("12341231")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

    
def shaping_coil_list(request):
    cw = None
    qw = None
    weight_consumed = None
    if request.method == "POST":
        try:
            cw = Decimal(request.POST.get("cw"))
            qw = Decimal(request.POST.get("qw"))
        except:
            messages.error(request, "Ne pas laisser le poids de contrôle vide, mettez le poids, ou mettez 0.")
            return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(shaper = request.user , status="PENDING_SHAPING")})

        if qw != 0 and cw != 0:
            messages.error(
                request, "Soit le poids de contôle, soit le poids en quarantaine, pas les deux en même temps !")
            return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(shaper = request.user , status="PENDING_SHAPING")})

        coil_slug = request.POST.get("get_coil")
        coil = get_object_or_404(Coil, slug=coil_slug)
        if coil.status == "IN_STOCK":
            messages.error(request, "Cette Bobine est déjà consommée")
            return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(shaper = request.user , status="PENDING_SHAPING")})
            
        if qw != 0:
            if qw == coil.weight:
                if coil.quarantine_level == 0:
                    coil.quarantine_level = coil.quarantine_level + 1
                    coil.status = "QUARANTINE"
                    
                elif coil.quarantine_level == 1:
                    coil.quarantine_level = coil.quarantine_level + 1
                    coil.status = "TO_BE_DESTROYED"

                production = Production.objects.get(coil = coil, process_type = "SHAPING", state = "PENDING")
                mchn = Machine.objects.get(slug=production.machine.slug)
                mchn.state = "FREE"
                mchn.save()
                coil.save()
                production.delete()
                return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(status="PENDING_SHAPING")})
            elif qw > coil.weight:
                messages.error(request, "Poids supérieur à celui de la bobine")
                return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(status="PENDING_SHAPING")})
            else:
                production = Production.objects.get(
                    coil=coil, process_type="SHAPING", state="PENDING")
                mchn = Machine.objects.get(slug=production.machine.slug)
                mchn.state = "FREE"
                mchn.save()
                coil.status = "CUT"
                coil.save()
                ref_consumed = get_random_string(15)
                ref_quarantine = get_random_string(15)
                weight_consumed = coil.weight - qw
                consumed_coil = Coil(user=coil.user, introducer = coil.introducer,type_name = coil.type_name,  type_coil = coil.type_coil, micronnage = coil.micronnage,supplier = coil.supplier, extrusion_machine = coil.extrusion_machine, printing_machine = coil.printing_machine, shaping_machine = coil.shaping_machine, creation_date = coil.creation_date, printing_date = coil.printing_date, shaping_date= coil.shaping_date, printer=coil.printer, shaper = coil.shaper, ref=ref_consumed, parent=coil, name=coil.name, capacity=coil.capacity, printed = coil.printed, 
                                     is_sub = True,color=coil.color, the_print=coil.the_print, perfume=coil.perfume, status="CONSUMED", weight=weight_consumed, cw1 = coil.cw1, cw2 = coil.cw2, cw3 = coil.cw3, cwm = coil.cwm, ticket_printed = True)
                quarantine_coil = Coil(quarantine_level = 1, user=coil.user, introducer = coil.introducer, type_name = coil.type_name, type_coil = coil.type_coil, micronnage = coil.micronnage, supplier = coil.supplier, extrusion_machine = coil.extrusion_machine, printing_machine = coil.printing_machine, shaping_machine = coil.shaping_machine, creation_date = coil.creation_date, printing_date = coil.printing_date, shaping_date= coil.shaping_date, printer=coil.printer, shaper=coil.shaper, ref=ref_quarantine, parent=coil, name=coil.name, capacity=coil.capacity, printed = coil.printed, 
                                       is_sub = True, color=coil.color, the_print=coil.the_print, perfume=coil.perfume, status="QUARANTINE", weight=qw, ticket_printed = True)
                production.coil = consumed_coil
                consumed_coil.save()
                quarantine_coil.save()
                production.save()
                return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(status="PENDING_SHAPING")})

        if coil.cw1 != 0 and coil.cw2 != 0 and coil.cw3 != 0:
            coil.status = "CONSUMED"
            production = Production.objects.get(
                coil=coil, process_type="SHAPING", state="PENDING")
            production.state = "FINISHED"
            mchn = Machine.objects.get(slug=production.machine.slug)
            mchn.state = "FREE"
            mchn.save()
            coil.save()
            production.save()
        if cw != 0:
            if coil.cw1 is None or coil.cw1 == 0:
                coil.cw1 = cw/1000
                coil.save()
            elif coil.cw2 is None or coil.cw2 == 0:
                coil.cw2 = cw/1000
                coil.save()
            elif coil.cw3 is None or coil.cw3 == 0:
                coil.cw3 = cw/1000
                coil.save()
            else:
                pass

    return render(request, 'production/shaping_coil_list.html', context={'object_list': Coil.objects.filter(status="PENDING_SHAPING")})

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Créer Bobine'
        return context


class MixingIndexView(TemplateView):
    template_name = 'production/index_mixing.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PersonnelIndexView(TemplateView):
    template_name = 'profile/index_personnel.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ConsultingIndexView(TemplateView):
    template_name = 'production/index_consulting.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ExtrusionIndexView(TemplateView):
    template_name = 'production/index_extrusion.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PrintingIndexView(TemplateView):
    template_name = 'production/index_printing.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ShapingIndexView(TemplateView):
    template_name = 'production/index_shaping.html'

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductMixingListView(ListView):
    queryset = RawMatter.objects.exclude(name__name="encre").filter(quantity_workshop__gt=0)
    context_object_name = 'product_list'
    template_name = 'stock_manager/stock_list.html'
    success_url = reverse_lazy('production:mixing-process')

    @ method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mélange'
        context["STOCK_TYPE"] = "STOCK_OUT"
        context["mixing_name"] = "mixing"
        return context



class MixingListView(ListView):

    template_name = 'production/mixing_list.html'

    def get_queryset(self, **kwargs):
        now = timezone.now()
        now_less = now.replace(day = 1)
        if now.month == 1 or now.month == 3 or now.month == 5 or now.month == 7 or now.month == 8 or now.month == 10 or now.month == 12:
            now_more = now.replace(day = 31)
        elif now.month == 4 or now.month == 6 or now.month == 9 or now.month == 11:
            now_more = now.replace(day = 30)
        elif now.month == 2:
            if now.year % 4 == 0:
                now_more = now.replace(day = 29)
            else:
                now_more = now.replace(day = 28)

        queryset = Order.objects.exclude(machine = None).filter(user=self.request.user)
        queryset = queryset.filter(ordered_date__lte = now_more )
        queryset = queryset.filter(ordered_date__gte = now_less )
        return queryset

class MyHolidaysListView(ListView):
    template_name = 'profile/list/my_holidays.html'
    def get_queryset(self, **kwargs):
        queryset = HolidayRequest.objects.filter(user__profile__group=self.request.user.profile.group)
        return queryset


def validate_production(request, slug):
    production = get_object_or_404(Production, slug=slug)
    production.state = "FINISHED"
    production.save()
    if production.process_type !="MIXING":
        mchn = Machine.objects.get(slug=production.machine.slug)
        mchn.state = "FREE"
        mchn.save()
    if production.process_type == "MIXING":
        return redirect(reverse_lazy("production:mixing-list"))
    elif production.process_type == "EXTRUSION":
        coil = production.coil
        coil.ext_validated = True
        coil.save()
        return redirect(reverse_lazy("production:extrusion-coil-list"))
    elif production.process_type == "PRINTING":
        return redirect(reverse_lazy("production:printing-list"))    
    elif production.process_type == "SHAPING":
        return redirect(reverse_lazy("production:shaping-list"))
    elif production.process_type == "FINISHED_PRODUCT":
        # return redirect (reverse_lazy("production:production-list"))
        pass

def delete_production(request, slug):
    production = coil = None
    try:
        production = get_object_or_404(Production, slug=slug)
    except:
        coil = get_object_or_404(Coil, slug=slug)

    if production is not None:

        if production.process_type !="MIXING":
            mchn = Machine.objects.get(slug=production.machine.slug)
            mchn.state = "FREE"
            mchn.save()
        if production.process_type == "MIXING":
            cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Mélange")
            cancellation.save()
            production.delete()
            return redirect(reverse_lazy("production:mixing-list"))
        elif production.process_type == "EXTRUSION":
            cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Extrusion")
            cancellation.save()
            coil = production.coil
            production.delete()
            coil.delete()
            return redirect(reverse_lazy("production:extrusion-list"))
        elif production.process_type == "PRINTING":
            cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Impression")
            cancellation.save()
            coil = production.coil
            coil.printing_date = None
            coil.printer = None
            coil.printing_machine = None
            coil.status = "IN_STOCK"
            production.delete()
            coil.save()
            return redirect(reverse_lazy("production:printing-list"))
        elif production.process_type == "SHAPING":
            cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Façonnage")
            cancellation.save()
            coil = production.coil
            coil.shaping_date = None
            coil.shaper = None
            coil.shaping_machine = None
            coil.status = "IN_STOCK"
            coil.cw1 = 0
            coil.cw2 = 0
            coil.cw3 = 0
            production.delete()
            coil.save()
            return redirect(reverse_lazy("production:shaping-list"))
        elif production.process_type == "FINISHED_PRODUCT":
            cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Production Produit Fini")
            cancellation.save()
            production.delete()
            return redirect (reverse_lazy("production:production-list"))
    elif coil is not None:
        cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Façonnage")
        cancellation.save()
        coil.shaping_date = None
        coil.shaper = None
        coil.shaping_machine = None
        coil.status = "IN_STOCK"
        coil.cw1 = 0
        coil.cw2 = 0
        coil.cw3 = 0
        production = get_object_or_404(Production, coil = coil, process_type = "SHAPING")
        production.machine.state = "FREE"
        production.machine.save()
        production.delete()
        coil.save()
        return redirect(reverse_lazy("production:shaping-coil-list"))

class TrashCreateView(View):
    model = Trash
    template_name = 'production/trash_create.html'
    success_url = reverse_lazy('production:trash-list')

    def get(self, request, *arg, **kwargs):
        if request.user.profile.job_position.name == "Opérateur Extrusion":
            form = ExtrusionTrashForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Façonnage":
            form = ShapingTrashForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Impression":
            form = PrintingTrashForm(request.POST)
        elif request.user.Profile.job_position.name == "Gestionnaire de Stock":
            form = GeneralTrashForm(request.POST)
        context = {
            'form': form,
        }
        return render(self.request, 'production/trash_create.html', context)

    def post(self, request, *args, **kwargs):

        if request.user.profile.job_position.name == "Opérateur Extrusion":
            form = ExtrusionTrashForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Façonnage":
            form = ShapingTrashForm(request.POST)
        elif request.user.profile.job_position.name == "Opérateur Impression":
            form = PrintingTrashForm(request.POST)
        elif request.user.Profile.job_position.name == "Gestionnaire de Stock":
            form = GeneralTrashForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                trash_type = form.trash_type
                machine = form.machine
                weight = form.weight
                user = request.user
                company = Company.objects.get(name="Ln Plast")
                ref = get_random_string(15)
                trash = Trash(ref=ref, date=timezone.now(), user=user, weight=weight, machine=machine, trash_type=trash_type, whereabouts=company, state="PENDING")
                trash.save()
                return redirect(self.success_url)
            else:
                pass

class InkConsumptionView(View):
    model = InkConsumption
    template_name = 'production/ink_consumption.html'
    success_url = reverse_lazy('production:index-printing')

    def get(self, request, *arg, **kwargs):
        form = InkConsumptionForm(request.POST)
        context = {
            'form': form,
        }
        return render(self.request, 'production/ink_consumption.html', context)

    def post(self, request, *args, **kwargs):

        form = InkConsumptionForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                machine = form.machine
                ink = form.ink
                quantity = form.quantity
                user = request.user
                if quantity == 0:
                    messages.error(request, "Quantité Non Acceptée !")
                    return redirect(reverse_lazy("production:ink-consumption"))

                rawmatter = RawMatter.objects.get(slug = ink.slug)
                try:
                    rawmatter.quantity_workshop = rawmatter.quantity_workshop - quantity
                    rawmatter.save()
                    ink_consumption = InkConsumption(date=timezone.now(), user=user, quantity=quantity, machine=machine, ink=ink)
                    ink_consumption.save()
                except:
                    messages.error(request, "Quantité Indisponible Dans L'Atelier !")
                    return redirect(reverse_lazy("production:ink-consumption"))


                return redirect(self.success_url)
            else:
                pass

class TrashListView(ListView):

    template_name = 'production/trash_list.html'

    def get_queryset(self, **kwargs):
        queryset = Trash.objects.filter(user=self.request.user, state = "PENDING")
        return queryset


class MachineStopListView(ListView):

    template_name = 'production/machine_stop_list.html'

    def get_queryset(self, **kwargs):
        queryset = MachineStop.objects.filter(user=self.request.user)
        return queryset

class HandleConsumptionListView(ListView):

    template_name = 'production/handle_consumption_list.html'

    def get_queryset(self, **kwargs):
        queryset = HandleConsumption.objects.filter(user=self.request.user)
        return queryset

class LabellingConsumptionListView(ListView):

    template_name = 'production/labelling_consumption_list.html'

    def get_queryset(self, **kwargs):
        queryset = LabellingConsumption.objects.filter(user=self.request.user)
        return queryset

def coil_issues(request):
    motive = None
    explanation = None
    coil = None
    coils = Coil.objects.filter(status="QUARANTINE") | Coil.objects.filter(defective="DEFECTIVE") | Coil.objects.exclude(destroyed=True).filter(status="TO_BE_DESTROYED")
    now = timezone.now()
    now = now.replace(hour = 0)
    coils = coils.filter(shaping_date__gte = now)
    if request.method == "POST":
        motive = request.POST.get("motive")
        explanation = request.POST.get("explanation")
        coil_slug = request.POST.get("get_coil")
        coil = get_object_or_404(Coil, slug=coil_slug)
        coil.motive = motive
        coil.explanation = explanation
        coil.save()
    return render(request, 'production/coil_issues.html', context={'object_list': coils})

def delete_trash(request, slug):
    trash = get_object_or_404(Trash, slug=slug)
    cancellation = Cancellation(date = timezone.now(), user = request.user, cancellation_type = "Déchet")
    cancellation.save()
    trash.delete()
    if request.user.profile.job_position.name == "Gestionnaire de Stock":
        return redirect (reverse_lazy("stock-manager:trash-validation"))
    else:
        return redirect (reverse_lazy("production:trash-list"))

def delete_machine_stop(request, slug):
    stop = get_object_or_404(MachineStop, slug=slug)
    stop.delete()
    return redirect (reverse_lazy("production:machine-stop-list"))

def delete_handle_consumption(request, slug):
    hc = get_object_or_404(HandleConsumption, slug=slug)
    handle = Handle.objects.get(slug = hc.handle.slug)
    handle.quantity_workshop += hc.quantity
    handle.save()
    hc.delete()
    return redirect (reverse_lazy("production:handle-consumption-list"))

def delete_labelling_consumption(request, slug):
    lc = get_object_or_404(LabellingConsumption, slug=slug)
    labelling = Labelling.objects.get(slug = lc.labelling.slug)
    labelling.quantity_workshop += lc.quantity
    labelling.save()
    lc.delete()
    return redirect (reverse_lazy("production:labelling-consumption-list"))

def defective_coil(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    if coil.cw1 == 0 or coil.cw2 == 0 or coil.cw3 == 0 or coil.cw1 is None or coil.cw2 is None or coil.cw3 is None:
        messages.error(request, "Veuillez introduire les poids de contrôle")
        return redirect(request.META.get('HTTP_REFERER'))
    coil.status = "CONSUMED"
    coil.defective = "DEFECTIVE"
    production = Production.objects.get(
        coil=coil, process_type="SHAPING", state="PENDING")
    production.state = "FINISHED"
    mchn = Machine.objects.get(slug=production.machine.slug)
    mchn.state = "FREE"
    mchn.save()
    coil.save()
    production.save()
    return redirect(reverse_lazy("production:shaping-coil-list"))

def reset_cws(request, slug):
    coil = get_object_or_404(Coil, slug=slug)
    coil.cw1 = 0
    coil.cw2 = 0
    coil.cw3 = 0

    coil.save()
    return redirect(reverse_lazy("production:shaping-coil-list"))


class ShapingCreateView(View):
    model = Production
    template_name = 'production/shaping.html'
    success_url = reverse_lazy('production:shaping-coil-list')

    def get(self, request, *arg, **kwargs):
        form = ShapingForm()
        context = {
            'form': form,
        }
        return render(self.request, 'production/shaping.html', context)

    def post(self, request, *args, **kwargs):
        form = ShapingForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                coil = None
                form = form.save(commit=False)
                product = request.POST.get('_ref')
                product2 = request.POST.get('_ref2')
                product3 = request.POST.get('_ref3')
                product4 = request.POST.get('_ref4')
                product5 = request.POST.get('_ref5')
                product6 = request.POST.get('_ref6')
                user = form.user
                try:
                    coil = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product)
                    coil_type = coil.type_coil
                except:
                    coil = None
                
                try:
                    coil2 = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product2)
                    coil_type2 = coil2.type_coil
                except:
                    coil2 = None
                
                try:
                    coil3 = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product3)
                    coil_type3 = coil3.type_coil
                except:
                    coil3 = None
                
                try:
                    coil4 = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product4)
                    coil_type4 = coil4.type_coil
                except:
                    coil4 = None

                try:
                    coil5 = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product5)
                    coil_type5 = coil5.type_coil
                except:
                    coil5 = None

                try:
                    coil6 = Coil.objects.exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").get(ref__icontains=product6)
                    coil_type6 = coil6.type_coil
                except:
                    coil6 = None

                if coil != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil, user=user, coil_type = coil_type ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil.status = "PENDING_SHAPING"
                    coil.shaper = shaping.user
                    coil.shaping_date = shaping.date
                    coil.shaping_machine = shaping.machine
                    coil.save()
                    mchn.save()
                    shaping.save()
                if coil2 != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil2, user=user, coil_type = coil_type2 ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil2.status = "PENDING_SHAPING"
                    coil2.shaper = shaping.user
                    coil2.shaping_date = shaping.date
                    coil2.shaping_machine = shaping.machine
                    coil2.save()
                    mchn.save()
                    shaping.save()
                if coil3 != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil3, user=user, coil_type = coil_type3 ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil3.status = "PENDING_SHAPING"
                    coil3.shaper = shaping.user
                    coil3.shaping_date = shaping.date
                    coil3.shaping_machine = shaping.machine
                    coil3.save()
                    mchn.save()
                    shaping.save()
                if coil4 != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil4, user=user, coil_type = coil_type4 ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil4.status = "PENDING_SHAPING"
                    coil4.shaper = shaping.user
                    coil4.shaping_date = shaping.date
                    coil4.shaping_machine = shaping.machine
                    coil4.save()
                    mchn.save()
                    shaping.save()
                if coil5 != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil5, user=user, coil_type = coil_type5 ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil5.status = "PENDING_SHAPING"
                    coil5.shaper = shaping.user
                    coil5.shaping_date = shaping.date
                    coil5.shaping_machine = shaping.machine
                    coil5.save()
                    mchn.save()
                    shaping.save()
                if coil6 != None:
                    machine = form.machine
                    shaping = Production(date=timezone.now(),coil = coil6, user=user, coil_type = coil_type6 ,quantity_produced=1, machine=machine, process_type="SHAPING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil6.status = "PENDING_SHAPING"
                    coil6.shaper = shaping.user
                    coil6.shaping_date = shaping.date
                    coil6.shaping_machine = shaping.machine
                    coil6.save()
                    mchn.save()
                    shaping.save()
                return redirect(self.success_url)

class HandleConsumptionView(View):
    model = HandleConsumption
    template_name = 'production/handle_consumption.html'
    success_url = reverse_lazy('production:handle-consumption')

    def get(self, request, *arg, **kwargs):
        form = HandleConsumptionForm()
        context = {
            'form': form,
        }
        return render(self.request, 'production/handle_consumption.html', context)

    def post(self, request, *args, **kwargs):
        form = HandleConsumptionForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                handle = form.handle

                if handle != None:
                    quantity = form.quantity
                    mchn = form.machine
                    machine = Machine.objects.get(slug=mchn.slug)
                    user = request.user
                    handle_consumption = HandleConsumption(date=timezone.now(), quantity = quantity, user=user, handle = handle, machine=machine)
                    if quantity <= handle.quantity_workshop:
                        handle.quantity_workshop = handle.quantity_workshop - quantity
                    else:
                        messages.error(
                        request, "Quantité Non Disponible En Stock")
                        return redirect(request.META.get('HTTP_REFERER'))
                    handle.save()
                    handle_consumption.save()
                    return redirect(self.success_url)
                else:
                    messages.error(
                        request, "Cordon inexistant")
                    return redirect(reverse_lazy("production:handle-consumption"))

class LabellingConsumptionView(View):
    model = LabellingConsumption
    template_name = 'production/labelling_consumption.html'
    success_url = reverse_lazy('production:labelling-consumption')

    def get(self, request, *arg, **kwargs):
        form = LabellingConsumptionForm()
        context = {
            'form': form,
        }
        return render(self.request, 'production/labelling_consumption.html', context)

    def post(self, request, *args, **kwargs):
        form = LabellingConsumptionForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                labelling = form.labelling

                if labelling != None:
                    quantity = form.quantity
                    mchn = form.machine
                    machine = Machine.objects.get(slug=mchn.slug)
                    user = request.user
                    labelling_consumption = LabellingConsumption(user = request.user, date = timezone.now(), labelling = labelling, machine = mchn, quantity = quantity)
                    if quantity <= labelling.quantity_workshop:
                        labelling.quantity_workshop = labelling.quantity_workshop - quantity
                    else:
                        messages.error(
                        request, "Quantité Non Disponible En Stock")
                        return redirect(request.META.get('HTTP_REFERER'))
                    labelling.save()
                    labelling_consumption.save()
                    return redirect(self.success_url)
                else:
                    messages.error(
                        request, "Labelling inexistant")
                    return redirect(reverse_lazy("production:labelling-consumption"))

class PrintingCreateView(View):
    model = Production
    template_name = 'production/printing.html'
    success_url = reverse_lazy('production:printing-coil-list')

    def get(self, request, *arg, **kwargs):
        form = PrintingForm()
        context = {
            'form': form,
        }
        return render(self.request, 'production/printing.html', context)

    def post(self, request, *args, **kwargs):
        form = PrintingForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                product = request.POST.get('_ref')
                try:
                    coil = Coil.objects.exclude(printed ="PRINTED").exclude(status ="TO_BE_DESTROYED").exclude(status ="CONSUMED").exclude(status ="SOLD").exclude(status ="CUT").exclude(status ="PENDING_EXTRUSION").exclude(status ="PENDING_PRINTING").exclude(status ="PENDING_SHAPING").exclude(status ="QUARANTINE").exclude(status ="PENDING_DATA").get(ref__icontains=product)
                except Coil.DoesNotExist:
                    coil = None
                if coil != None:
                    # if coil.name.name != "médical":
                    #     coil_name = Range.objects.get(name = "médical")
                    #     coil.name = coil_name
                    #     typeofcoil = CoilType.objects.get(name = coil_name, capacity = coil.capacity, color = coil.color, the_print = coil.the_print)
                    #     coil.type_coil = typeofcoil
                    #     coil.save()
                    machine = form.machine
                    the_print = form.the_print
                    user = request.user
                    coil_type = coil.type_coil
                    printing = Production(date=timezone.now(), coil = coil, user=user, coil_type=coil_type, quantity_produced=1, machine=machine, process_type="PRINTING", state="PENDING")
                    mchn = Machine.objects.get(slug=machine.slug)
                    mchn.state = "OCCUPIED"
                    coil.status = "PENDING_PRINTING"
                    coil.printer = request.user
                    coil.printing_date = printing.date
                    coil.printing_machine = printing.machine
                    coil.the_print = the_print
                    coil.save()
                    mchn.save()
                    printing.save()
                    return redirect(self.success_url)
                else:
                    messages.error(
                        request, "Référence Inexistante")
                    return redirect(reverse_lazy("production:printing-process"))


class FinishedProductCreateView(View):
    model = Production
    template_name = 'production/finished_product.html'
    success_url = reverse_lazy('production:production-list')

    def get(self, request, *arg, **kwargs):
        form = FinishedProductForm()
        context = {
            'form': form,
            'ranges':Range.objects.all(),
            'colors':Color.objects.all(),
            'flavors':Flavor.objects.all(),
        }
        return render(self.request, 'production/finished_product.html', context)

    def post(self, request, *args, **kwargs):
        form = FinishedProductForm(request.POST)

        if self.request.method == "POST":
            if form.is_valid():
                form = form.save(commit=False)
                # product_range = request.POST.get("range")
                # product_capacity = request.POST.get("capacity")
                # try:
                #     product_capacity = int(product_capacity)
                # except:
                #     messages.error(request, "Veuillez choisir la capacité")
                #     return redirect(request.META.get('HTTP_REFERER'))
                # product_color = request.POST.get("color")
                # product_link = request.POST.get("link")
                # product_perfume = request.POST.get("perfume")
                # product_flavor = request.POST.get("flavor")
                # if product_flavor == "None" : product_flavor = None

                # print(product_range, "-",product_capacity, "-", product_color, "-", product_link, "-", product_perfume, "-", product_flavor)
                # try:
                #     product_confirmation = FinishedProductType.objects.get(name__slug = product_range, capacity = product_capacity, color__name = product_color, link = product_link, perfume = product_perfume, flavor__name = product_flavor )
                # except:
                #     messages.error(request, "Produit Introuvable")
                #     return redirect(request.META.get('HTTP_REFERER'))
                user = form.user
                user2 = form.user2
                user3 = form.user3
                product = form.product
                machine = form.machine
                quantity = form.quantity_produced
                production = Production(date=timezone.now(), user=user, user2 = user2, user3 = user3, product=product, quantity_produced=quantity,
                                        machine=machine, process_type="FINISHED_PRODUCT", state="PENDING")
                production.save()
                return redirect(self.success_url)
            else:
                pass


class ShapingListView(ListView):

    template_name = 'production/pending_shaping.html'

    def get_queryset(self, **kwargs):
        queryset = Production.objects.filter(
            user=self.request.user, state="PENDING", process_type="SHAPING")
        return queryset

class ProductionListView(ListView):

    template_name = 'production/pending_production.html'

    def get_queryset(self, **kwargs):
        queryset = Production.objects.filter(
            state="PENDING", process_type="FINISHED_PRODUCT")
        return queryset


class PrintingListView(ListView):

    template_name = 'production/pending_printing.html'

    def get_queryset(self, **kwargs):
        queryset = Production.objects.filter(
            user=self.request.user, state="PENDING", process_type="PRINTING")
        return queryset


def printing_coil_list(request):
    lm = timezone.now()
    if lm.month != 1:
        month = lm.month - 1
        year = lm.year
    else:
        month = 12
        year = lm.year - 1
    lm = lm.replace(day = 1, month=month, year=year)
    weight = 0
    coils = Coil.objects.filter(status = "PENDING_PRINTING") | Coil.objects.filter(is_sub = True, printing_date__gte = lm)
    now = timezone.now()
    now = now.replace(hour = 0)
    # coils = coils.filter(printing_date__gte = now)
    if request.method == "POST":
        coil_slug = request.POST.get("get_coil")
        coil = get_object_or_404(Coil, slug=coil_slug)
        micronnage_print = request.POST.get("micronnage")
        production = Production.objects.get(process_type="PRINTING",coil=coil, state="PENDING")
        production.state = "FINISHED"
        production.save()
        coil.status = "IN_STOCK"
        coil.printed = "PRINTED"
        coil.micronnage_print = micronnage_print
        coil.save()
        mchn = Machine.objects.get(slug=production.machine.slug)
        mchn.state = "FREE"
        mchn.save()
        return render(request, 'production/printing_coil_list.html', context={'object_list': coils })

    return render(request, 'production/printing_coil_list.html', context={'object_list': coils })

class RecapPage(View):
    template_name = 'production/recap_page.html'

    def get(self, request):
        return render(request, "production/recap_page.html")

class AdminRecapPage(View):
    template_name = 'production/admin_recap_page.html'

    def get(self, request):
        return render(request, "production/admin_recap_page.html", context={"job_positions": JobPosition.objects.exclude(name="Administrateur").exclude(name="Gérant").all()})


def recap(request):
    current_time = None
    morning = None
    evening = None
    night = None
    if request.method == "GET":
        date_str = request.GET.get("date")
        current_time = parse_date(date_str)
        if current_time == None:
            messages.error(request, 'Veuillez choisir la date')
            return redirect(request.META.get('HTTP_REFERER'))
        current_time = datetime.combine(current_time, datetime.min.time())

        morning = request.GET.get("morning")
        evening = request.GET.get("evening")
        night = request.GET.get("night")

        if (morning == 'on' and night == 'on') or (morning == 'on' and evening == 'on') or (evening == 'on' and night == 'on'):
            messages.error(request, 'Veuillez choisir une seule : matinée, après midi ou nuit.')
            return redirect(request.META.get('HTTP_REFERER'))
        if morning == None and evening == None and night == None:
            messages.error(request, 'Veuillez choisir une : matinée, après midi ou nuit.')
            return redirect(request.META.get('HTTP_REFERER'))

        if morning == 'on':
            if request.user.profile.job_position.name == "Mélangeur":
                start_time = current_time.replace(hour = 7, minute = 0, second = 0, microsecond = 0)
                finish_time = current_time.replace(hour = 18, minute = 0, second = 0, microsecond = 0)
            else:
                start_time = current_time.replace(hour = 6, minute = 5, second = 0, microsecond = 0)
                finish_time = current_time.replace(hour = 14, minute = 10, second = 0, microsecond = 0)
        elif evening == 'on':
            start_time = current_time.replace(hour = 14, minute = 5, second = 0, microsecond = 0)
            finish_time = current_time.replace(hour = 22, minute = 10, second = 0, microsecond = 0)
        elif night == 'on':
            start_time = current_time.replace(hour = 22, minute = 5, second = 0, microsecond = 0)
            finish_time = current_time.replace(hour = 6, minute = 10, second = 0, microsecond = 0)
            if current_time.month == 1 or current_time.month == 3 or current_time.month == 5 or current_time.month == 7 or current_time.month == 8 or current_time.month == 10:
                if current_time.day == 31:
                    finish_time = finish_time.replace(day = 1)
                    month = current_time.month + 1
                    finish_time = finish_time.replace(month = month)
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 4 or current_time.month == 6 or current_time.month == 9 or current_time.month == 11:
                if current_time.day == 30:
                    finish_time = finish_time.replace(day = 1)
                    month = current_time.month + 1
                    finish_time = finish_time.replace(month = month)
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 12:
                if current_time.day == 31:
                    year = current_time.year + 1
                    finish_time = finish_time.replace(day = 1, month = 1, year = year )
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 2:
                if current_time.day == 28:
                    if current_time.year % 4 == 0:
                        day = current_time.day + 1
                        finish_time = finish_time.replace(day = day)
                    else:
                        finish_time = finish_time.replace(day = 1, month = 3)
                elif current_time.day == 29:
                    finish_time = finish_time.replace(day = 1, month = 3)
                else:
                    day = finish_time.day + 1
                    finish_time = finish_time.replace(day = day)
    

        if request.user.profile.job_position.name == "Opérateur Extrusion":
        
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Coil List #######################
            coil_list = Coil.objects.filter(user = request.user)
            coil_list = coil_list.filter(creation_date__gte = start_time)
            coil_list = coil_list.filter(creation_date__lte = finish_time)
            coil_total = 0
            for coil in coil_list:
                coil_total += coil.weight
            
            previous_coil_list = Coil.objects.exclude(user = request.user).filter(introducer = request.user)
            previous_coil_list = previous_coil_list.filter(creation_date__gte = start_time)
            previous_coil_list = previous_coil_list.filter(creation_date__lte = finish_time)

            ####################### Printed Coil List #######################
            printed_coil_list = Coil.objects.filter(printer = request.user)
            printed_coil_list = printed_coil_list.filter(printing_date__gte = start_time)
            printed_coil_list = printed_coil_list.filter(printing_date__lte = finish_time)
            printed_coil_total = 0
            for coil in printed_coil_list:
                if coil.status != "CUT":
                    printed_coil_total += coil.weight

            ####################### Trash Total #####################
    
            trash_list = Trash.objects.filter(user = request.user, machine__machine_type__name="Extrudeuse") | Trash.objects.filter(user = request.user, machine__machine_type__name="Imprimeuse")
            trash_list = trash_list.filter(date__gte = start_time)
            trash_list = trash_list.filter(date__lte = finish_time)
            total_trash = 0
            for trash in trash_list:
                total_trash += trash.weight
    
            ###################### Machine Stops #####################
            stop_list = MachineStop.objects.filter(user = request.user, machine__machine_type__name="Extrudeuse") | MachineStop.objects.filter(user = request.user, machine__machine_type__name="Imprimeuse")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration
    
            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": request.user,
                "coil_list": coil_list,
                "previous_coil_list": previous_coil_list,
                "printed_coil_list": printed_coil_list,
                "printed_coil_total": printed_coil_total,
                "coil_total": coil_total,
                "company": company,
                "type": "Extrusion",
                "trash_list": trash_list,
                "stop_list": stop_list,
                "trash": total_trash,
                "stop": total_stop,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_ext_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
    
        elif request.user.profile.job_position.name == "Opérateur Façonnage":
    
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Coil List #######################
            coil_list = Coil.objects.filter(shaper = request.user)
            coil_list = coil_list.filter(shaping_date__gte = start_time)
            coil_list = coil_list.filter(shaping_date__lte = finish_time)
            coil_total = 0
            for coil in coil_list:
                if coil.status == "CONSUMED":
                    coil_total += coil.weight
            
            ####################### Product List #######################
            products = FinishedProductType.objects.all()
            for i in range(products.__len__()):
                products[i].calculated_quantity_produced = products[i].user_quantity_produced(start_time, finish_time, request.user)
            ####################### Trash Total #####################
    
            trash_list = Trash.objects.filter(user = request.user, machine__machine_type__name="Soudeuse")
            trash_list = trash_list.filter(date__gte = start_time)
            trash_list = trash_list.filter(date__lte = finish_time)
            total_trash = 0
            for trash in trash_list:
                total_trash += trash.weight
    
            stop_list = MachineStop.objects.filter(user = request.user, machine__machine_type__name="Soudeuse")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration
    
            productions = Production.objects.filter(user = request.user, process_type = "FINISHED_PRODUCT")
            productions = productions.filter(date__gte = start_time)
            productions = productions.filter(date__lte = finish_time)
    
            production_total = 0
    
            for production in productions:
                production_total += production.quantity_produced
                    
    
            handle_consumptions = HandleConsumption.objects.filter(user = request.user)
            handle_consumptions = handle_consumptions.filter(date__gte = start_time)
            handle_consumptions = handle_consumptions.filter(date__lte = finish_time)
    
            handle_consumption_total = 0
    
            for handle_consumption in handle_consumptions:
                handle_consumption_total += handle_consumption.quantity
    
    
            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": request.user,
                "coil_list": coil_list,
                "products":products,
                "coil_total": coil_total,
                "company": company,
                "trash_list": trash_list,
                "trash": total_trash,
                "stop_list": stop_list,
                "stop": total_stop,
                "type": "Façonnage",
                "production_list": productions,
                "production": production_total,
                "handle_consumption_list" : handle_consumptions,
                "handle_consumption": handle_consumption_total,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_soud_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
    
        elif request.user.profile.job_position.name == "Mélangeur":
    
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Production List #######################

            order_list = Order.objects.filter(user = request.user)
            order_list = order_list.filter(ordered_date__gte = start_time)
            order_list = order_list.filter(ordered_date__lte = finish_time)
            
    
            stop_list = MachineStop.objects.filter(user = request.user, machine__machine_type__name="Mélangeur")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration

            raw_matters = RawMatter.objects.all()
            for i in range(raw_matters.__len__()):
                raw_matters[i].calculated_quantity_consumed = raw_matters[i].quantity_consumed(start_time, finish_time)
    
            orders = Order.objects.filter(intern_user = request.user)
            orders = orders.filter(ordered_date__gte = start_time)
            orders = orders.filter(ordered_date__lte = finish_time)
            orders_total = 0
            for order in orders:
                orders_total += order.get_total()

            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": request.user,
                "company": company,
                "type": "Mélange",
                "stop_list": stop_list,
                "stop": total_stop,
                "raw_matters": raw_matters,
                "orders": orders,
                "order_list":order_list,
                "orders_total":orders_total,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_mix_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
            
        @ method_decorator(login_required(login_url=reverse_lazy('login')))
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


def admin_recap(request):
    current_time = None
    morning = None
    evening = None
    night = None
    if request.method == "GET":
        date_str = request.GET.get("date")
        current_time = parse_date(date_str)
        if current_time == None:
            messages.error(request, 'Veuillez choisir la date')
            return redirect(request.META.get('HTTP_REFERER'))
        current_time = datetime.combine(current_time, datetime.min.time())

        morning = request.GET.get("morning")
        evening = request.GET.get("evening")
        night = request.GET.get("night")

        user_first = request.GET.get("user-first")
        user_last = request.GET.get("user-last")
        user_job = request.GET.get("user-job")
        try:
            user = User.objects.get(first_name__icontains = user_first, last_name__icontains = user_last, profile__job_position__slug = user_job)
        except:
            messages.error(request, "Aucun employé trouvé, veuillez vérifier le nom")
            return redirect(request.META.get('HTTP_REFERER'))

        if (morning == 'on' and night == 'on') or (morning == 'on' and evening == 'on') or (evening == 'on' and night == 'on'):
            messages.error(request, 'Veuillez choisir une seule : matinée, après midi ou nuit.')
            return redirect(request.META.get('HTTP_REFERER'))
        if morning == None and evening == None and night == None:
            messages.error(request, 'Veuillez choisir une : matinée, après midi ou nuit.')
            return redirect(request.META.get('HTTP_REFERER'))

        if morning == 'on':
            if user.profile.job_position.name == "Mélangeur":
                start_time = current_time.replace(hour = 7, minute = 0, second = 0, microsecond = 0)
                finish_time = current_time.replace(hour = 18, minute = 0, second = 0, microsecond = 0)
            else:
                start_time = current_time.replace(hour = 6, minute = 5, second = 0, microsecond = 0)
                finish_time = current_time.replace(hour = 14, minute = 10, second = 0, microsecond = 0)
        elif evening == 'on':
            start_time = current_time.replace(hour = 14, minute = 5, second = 0, microsecond = 0)
            finish_time = current_time.replace(hour = 22, minute = 10, second = 0, microsecond = 0)
        elif night == 'on':
            start_time = current_time.replace(hour = 22, minute = 5, second = 0, microsecond = 0)
            finish_time = current_time.replace(hour = 6, minute = 10, second = 0, microsecond = 0)
            if current_time.month == 1 or current_time.month == 3 or current_time.month == 5 or current_time.month == 7 or current_time.month == 8 or current_time.month == 10:
                if current_time.day == 31:
                    finish_time = finish_time.replace(day = 1)
                    month = current_time.month + 1
                    finish_time = finish_time.replace(month = month)
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 4 or current_time.month == 6 or current_time.month == 9 or current_time.month == 11:
                if current_time.day == 30:
                    finish_time = finish_time.replace(day = 1)
                    month = current_time.month + 1
                    finish_time = finish_time.replace(month = month)
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 12:
                if current_time.day == 31:
                    year = current_time.year + 1
                    finish_time = finish_time.replace(day = 1, month = 1, year = year )
                else:
                    day = current_time.day + 1
                    finish_time = finish_time.replace(day = day)
            elif current_time.month == 2:
                if current_time.day == 28:
                    if current_time.year % 4 == 0:
                        day = current_time.day + 1
                        finish_time = finish_time.replace(day = day)
                    else:
                        finish_time = finish_time.replace(day = 1, month = 3)
                elif current_time.day == 29:
                    finish_time = finish_time.replace(day = 1, month = 3)
                else:
                    day = finish_time.day + 1
                    finish_time = finish_time.replace(day = day)
    

        if user.profile.job_position.name == "Opérateur Extrusion":
        
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Coil List #######################
            coil_list = Coil.objects.filter(user = user)
            coil_list = coil_list.filter(creation_date__gte = start_time)
            coil_list = coil_list.filter(creation_date__lte = finish_time)
            coil_total = 0
            for coil in coil_list:
                coil_total += coil.weight
            
            previous_coil_list = Coil.objects.exclude(user = user).filter(introducer = user)
            previous_coil_list = previous_coil_list.filter(creation_date__gte = start_time)
            previous_coil_list = previous_coil_list.filter(creation_date__lte = finish_time)

            ####################### Printed Coil List #######################
            printed_coil_list = Coil.objects.filter(printer = user)
            printed_coil_list = printed_coil_list.filter(printing_date__gte = start_time)
            printed_coil_list = printed_coil_list.filter(printing_date__lte = finish_time)
            printed_coil_total = 0
            for coil in printed_coil_list:
                if coil.status != "CUT":
                    printed_coil_total += coil.weight

            ####################### Trash Total #####################
    
            trash_list = Trash.objects.filter(user = user, machine__machine_type__name="Extrudeuse") | Trash.objects.filter(user = user, machine__machine_type__name="Imprimeuse")
            trash_list = trash_list.filter(date__gte = start_time)
            trash_list = trash_list.filter(date__lte = finish_time)
            total_trash = 0
            for trash in trash_list:
                total_trash += trash.weight
    
            ###################### Machine Stops #####################
            stop_list = MachineStop.objects.filter(user = user, machine__machine_type__name="Extrudeuse") | MachineStop.objects.filter(user = user, machine__machine_type__name="Imprimeuse")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration
    
            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": user,
                "coil_list": coil_list,
                "previous_coil_list": previous_coil_list,
                "printed_coil_list": printed_coil_list,
                "printed_coil_total": printed_coil_total,
                "coil_total": coil_total,
                "company": company,
                "type": "Extrusion",
                "trash_list": trash_list,
                "stop_list": stop_list,
                "trash": total_trash,
                "stop": total_stop,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_ext_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
    
        elif user.profile.job_position.name == "Opérateur Façonnage":
    
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Coil List #######################
            coil_list = Coil.objects.filter(shaper = user)
            coil_list = coil_list.filter(shaping_date__gte = start_time)
            coil_list = coil_list.filter(shaping_date__lte = finish_time)
            coil_total = 0
            for coil in coil_list:
                if coil.status == "CONSUMED":
                    coil_total += coil.weight
            
            ####################### Product List #######################
            products = FinishedProductType.objects.all()
            for i in range(products.__len__()):
                products[i].calculated_quantity_produced = products[i].user_quantity_produced(start_time, finish_time, user)
            ####################### Trash Total #####################
    
            trash_list = Trash.objects.filter(user = user, machine__machine_type__name="Soudeuse")
            trash_list = trash_list.filter(date__gte = start_time)
            trash_list = trash_list.filter(date__lte = finish_time)
            total_trash = 0
            for trash in trash_list:
                total_trash += trash.weight
    
            stop_list = MachineStop.objects.filter(user = user, machine__machine_type__name="Soudeuse")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration
    
            productions = Production.objects.filter(user = user, process_type = "FINISHED_PRODUCT")
            productions = productions.filter(date__gte = start_time)
            productions = productions.filter(date__lte = finish_time)
    
            production_total = 0
    
            for production in productions:
                production_total += production.quantity_produced
                    
    
            handle_consumptions = HandleConsumption.objects.filter(user = user)
            handle_consumptions = handle_consumptions.filter(date__gte = start_time)
            handle_consumptions = handle_consumptions.filter(date__lte = finish_time)
    
            handle_consumption_total = 0
    
            for handle_consumption in handle_consumptions:
                handle_consumption_total += handle_consumption.quantity
    
    
            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": user,
                "coil_list": coil_list,
                "products":products,
                "coil_total": coil_total,
                "company": company,
                "trash_list": trash_list,
                "trash": total_trash,
                "stop_list": stop_list,
                "stop": total_stop,
                "type": "Façonnage",
                "production_list": productions,
                "production": production_total,
                "handle_consumption_list" : handle_consumptions,
                "handle_consumption": handle_consumption_total,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_soud_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
    
        elif user.profile.job_position.name == "Mélangeur":
    
            company = Company.objects.filter(name ="Ln Plast")[0]
            ####################### Production List #######################

            order_list = Order.objects.filter(user = user)
            order_list = order_list.filter(ordered_date__gte = start_time)
            order_list = order_list.filter(ordered_date__lte = finish_time)
            
    
            stop_list = MachineStop.objects.filter(user = user, machine__machine_type__name="Mélangeur")
            stop_list = stop_list.filter(date__gte = start_time)
            stop_list = stop_list.filter(date__lte = finish_time)
            total_stop = 0
            for stop in stop_list:
                total_stop += stop.duration

            raw_matters = RawMatter.objects.all()
            for i in range(raw_matters.__len__()):
                raw_matters[i].calculated_quantity_consumed = raw_matters[i].quantity_consumed(start_time, finish_time)
    
            orders = Order.objects.filter(intern_user = user)
            orders = orders.filter(ordered_date__gte = start_time)
            orders = orders.filter(ordered_date__lte = finish_time)
            orders_total = 0
            for order in orders:
                orders_total += order.get_total()

            template = loader.get_template('production/recap.html')
            context = {
                "start_time": start_time,
                "finish_time": finish_time,
                "user": user,
                "company": company,
                "type": "Mélange",
                "stop_list": stop_list,
                "stop": total_stop,
                "raw_matters": raw_matters,
                "orders": orders,
                "order_list":order_list,
                "orders_total":orders_total,
            }
            html = template.render(context)
            pdf = render_to_pdf('production/recap.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "recap_mix_%s.pdf" % (timezone.now())
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
            
        @ method_decorator(login_required(login_url=reverse_lazy('login')))
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context