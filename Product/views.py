from django.contrib.auth.decorators import login_required
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
from Product.models import Brand, Product, Color, Flavor, Coil, RawMatter, CoilType, FinishedProductType, Range, CombinedRange, Handle, Labelling, Package, Tape, SparePart

from Product.forms import (
    ColorForm,
    FlavorForm,
    RawMatterForm,
    CoilTypeForm,
    FinalProductForm,
    HandleForm,
    LabellingForm,
    PackageForm,
    TapeForm,
    SparePartForm,
    BrandForm,
    RangeForm,
    CombinedRangeForm,
)

class IndexConsumablesView(TemplateView):
    template_name = 'product/index_consumables.html'
    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
## --------------------------Handle------------------------##


class HandleCreateView(CreateView):
    model = Handle
    template_name = 'product/add_update/handle_add.html'
    form_class = HandleForm
    success_url = reverse_lazy('product:handles')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Cordon'
        return context

class HandleUpdateView(UpdateView):
    template_name = 'product/add_update/handle_add.html'
    form_class = HandleForm
    success_url = reverse_lazy('product:handles')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Cordon'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Handle, slug=_slug)

class HandleListView(ListView):
    template_name = 'product/list/handle_list.html'
    # paginate_by = 10
    queryset = Handle.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class HandleDeleteView(DeleteView):
    template_name = 'product/delete/handle_delete.html'
    success_url = reverse_lazy('product:handles')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Handle, slug=_slug)

#---------------------------End Handle------------------------##


## --------------------------Labelling------------------------##


class LabellingCreateView(CreateView):
    model = Handle
    template_name = 'product/add_update/labelling_add.html'
    form_class = LabellingForm
    success_url = reverse_lazy('product:labellings')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Labelling'
        return context

class LabellingUpdateView(UpdateView):
    template_name = 'product/add_update/labelling_add.html'
    form_class = LabellingForm
    success_url = reverse_lazy('product:labellings')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Labelling'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Labelling, slug=_slug)

class LabellingListView(ListView):
    template_name = 'product/list/labelling_list.html'
    # paginate_by = 10
    queryset = Labelling.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class LabellingDeleteView(DeleteView):
    template_name = 'product/delete/labelling_delete.html'
    success_url = reverse_lazy('product:labellings')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Labelling, slug=_slug)

#---------------------------End Labelling------------------------##


## --------------------------Packaging------------------------##


class PackageCreateView(CreateView):
    model = Package
    template_name = 'product/add_update/package_add.html'
    form_class = PackageForm
    success_url = reverse_lazy('product:packages')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouvel Emballage'
        return context

class PackageUpdateView(UpdateView):
    template_name = 'product/add_update/package_add.html'
    form_class = PackageForm
    success_url = reverse_lazy('product:packages')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Emballage'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Package, slug=_slug)

class PackageListView(ListView):
    template_name = 'product/list/package_list.html'
    # paginate_by = 10
    queryset = Package.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PackageDeleteView(DeleteView):
    template_name = 'product/delete/package_delete.html'
    success_url = reverse_lazy('product:packages')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Package, slug=_slug)

#---------------------------End Packaging------------------------##

## --------------------------Tape------------------------##


class TapeCreateView(CreateView):
    model = Tape
    template_name = 'product/add_update/tape_add.html'
    form_class = TapeForm
    success_url = reverse_lazy('product:tapes')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Scotch'
        return context

class TapeUpdateView(UpdateView):
    template_name = 'product/add_update/tape_add.html'
    form_class = TapeForm
    success_url = reverse_lazy('product:tapes')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Scotch'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Tape, slug=_slug)

class TapeListView(ListView):
    template_name = 'product/list/tape_list.html'
    # paginate_by = 10
    queryset = Tape.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class TapeDeleteView(DeleteView):
    template_name = 'product/delete/tape_delete.html'
    success_url = reverse_lazy('product:tapes')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Tape, slug=_slug)

#---------------------------End Tape------------------------##


#---------------------------Spare Parts------------------------##

class PartCreateView(CreateView):
    model = SparePart
    template_name = 'product/add_update/part_add.html'
    form_class = SparePartForm
    success_url = reverse_lazy('product:parts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Pièce de Rechange'
        return context

class PartUpdateView(UpdateView):
    template_name = 'product/add_update/part_add.html'
    form_class = SparePartForm
    success_url = reverse_lazy('product:parts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour une Pièce de Rechange'
        return context

    def get_object(self):
        _ref = self.kwargs.get('ref')
        return get_object_or_404(SparePart, ref=_ref)

class PartListView(ListView):
    template_name = 'product/list/part_list.html'
    # paginate_by = 10
    queryset = SparePart.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PartDeleteView(DeleteView):
    template_name = 'product/delete/part_delete.html'
    success_url = reverse_lazy('product:parts')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _ref = self.kwargs.get('ref')
        return get_object_or_404(SparePart, ref=_ref)


#---------------------------End Spart Parts------------------------##

class ProductIndexView(TemplateView):
    template_name = 'product/index.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# ##------------------------- Brand Views -------------------------##


class BrandCreateView(CreateView):
    model = Brand
    template_name = 'product/add_update/brand_add.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Marque'
        return context


class BrandUpdateView(UpdateView):
    template_name = 'product/add_update/brand_add.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour une Marque'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Brand, slug=_slug)


class BrandListView(ListView):
    queryset = Brand.objects.all()
    template_name = 'product/list/brand_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BrandDeleteView(DeleteView):
    template_name = 'product/delete/brand_delete.html'
    form_class = BrandForm
    success_url = reverse_lazy('product:brands')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Brand, slug=_slug)

# ##----------------------- End Brand Form -----------------------##

# ##------------------------- Range Views -------------------------##


class RangeCreateView(CreateView):
    model = Range
    template_name = 'product/add_update/range_add.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Gamme'
        return context


class RangeUpdateView(UpdateView):
    template_name = 'product/add_update/range_add.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour Une Gamme'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Range, slug=_slug)


class RangeListView(ListView):
    queryset = Range.objects.all()
    template_name = 'product/list/range_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RangeDeleteView(DeleteView):
    template_name = 'product/delete/range_delete.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Range, slug=_slug)

# ##----------------------- End Range Form -----------------------##


# ##------------------------- Combined Range Views -------------------------##


class CombinedRangeCreateView(CreateView):
    model = CombinedRange
    template_name = 'product/add_update/c_range_add.html'
    form_class = CombinedRangeForm
    success_url = reverse_lazy('product:c-ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Gamme Combinée'
        return context


class CombinedRangeUpdateView(UpdateView):
    template_name = 'product/add_update/c_range_add.html'
    form_class = CombinedRangeForm
    success_url = reverse_lazy('product:c-ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour Une Gamme Combinée'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(CombinedRange, slug=_slug)


class CombinedRangeListView(ListView):
    queryset = CombinedRange.objects.all()
    template_name = 'product/list/c_range_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CombinedRangeDeleteView(DeleteView):
    template_name = 'product/delete/c_range_delete.html'
    form_class = RangeForm
    success_url = reverse_lazy('product:c-ranges')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(CombinedRange, slug=_slug)

# ##----------------------- End Combined Range Form -----------------------##


##--------------------------- Color Form --------------------------##


class ColorCreateView(CreateView):
    model = Color
    template_name = 'product/add_update/color_add.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Couleur'
        return context


class ColorUpdateView(UpdateView):
    template_name = 'product/add_update/color_add.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour une Couleur'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Color, slug=_slug)


class ColorListView(ListView):
    queryset = Color.objects.all()
    template_name = 'product/list/color_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ColorDeleteView(DeleteView):
    template_name = 'product/delete/color_delete.html'
    form_class = ColorForm
    success_url = reverse_lazy('product:colors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Color, slug=_slug)
##------------------------- End color Form ------------------------##




##--------------------------- Flavor Form --------------------------##


class FlavorCreateView(CreateView):
    model = Flavor
    template_name = 'product/add_update/flavor_add.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Parfum'
        return context


class FlavorUpdateView(UpdateView):
    template_name = 'product/add_update/flavor_add.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Parfum'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Flavor, slug=_slug)


class FlavorListView(ListView):
    queryset = Flavor.objects.all()
    template_name = 'product/list/flavor_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FlavorDeleteView(DeleteView):
    template_name = 'product/delete/flavor_delete.html'
    form_class = FlavorForm
    success_url = reverse_lazy('product:flavors')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Flavor, slug=_slug)
##------------------------- End Flavor Form ------------------------##


##------------------------- Product Form ------------------------##


class CoilCreateView(CreateView):
    model = Coil
    template_name = 'product/add_update/coil_add.html'
    form_class = CoilTypeForm
    success_url = reverse_lazy('product:coils')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Bobine'
        return context


class RawMatterCreateView(CreateView):
    model = RawMatter
    template_name = 'product/add_update/rawmatter_add.html'
    form_class = RawMatterForm
    success_url = reverse_lazy('product:rawmatters')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter une Nouvelle Matière Première'
        return context


class FinalProductCreateView(CreateView):
    model = FinishedProductType
    template_name = 'product/add_update/finalproduct_add.html'
    form_class = FinalProductForm
    success_url = reverse_lazy('product:products')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Ajouter un Nouveau Produit Fini'
        return context


class CoilUpdateView(UpdateView):
    template_name = 'product/add_update/coil_add.html'
    form_class = CoilTypeForm
    success_url = reverse_lazy('product:coils')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour une Bobine'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(CoilType, slug=_slug)


class RawMatterUpdateView(UpdateView):
    template_name = 'product/add_update/rawmatter_add.html'
    form_class = RawMatterForm
    success_url = reverse_lazy('product:rawmatters')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à Jour une Matière Première'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(RawMatter, slug=_slug)


class FinalProductUpdateView(UpdateView):
    template_name = 'product/add_update/finalproduct_add.html'
    form_class = FinalProductForm
    success_url = reverse_lazy('product:products')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'Mettre à jour un Produit Fini'
        return context

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(FinishedProductType, slug=_slug)

# class ConsumablesUpdateView(UpdateView):
#     template_name = 'product/add_update/product_add.html'
#     form_class = ConsumablesForm
#     success_url = reverse_lazy('product:products')

#     @method_decorator(login_required(login_url=reverse_lazy('login')))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form_name"] = 'Mettre a Jour une pièce consommable'
#         return context

#     def get_object(self):
#         _slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, slug=_slug)

# class SparePartsUpdateView(UpdateView):
#     template_name = 'product/add_update/spareparts_add.html'
#     form_class = SparePartsForm
#     success_url = reverse_lazy('product:products')

#     @method_decorator(login_required(login_url=reverse_lazy('login')))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form_name"] = 'Mettre a Jour une pièce de rechange'
#         return context

#     def get_object(self):
#         _slug = self.kwargs.get('slug')
#         return get_object_or_404(Product, slug=_slug)


class FinalProductListView(ListView):
    #queryset = Product.objects.filter(category=Category.objects.get(name="produit finis").id)
    template_name = 'product/list/final_product_list.html'
    # paginate_by = 10
    queryset = FinishedProductType.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RawMatterListView(ListView):
    template_name = 'product/list/raw_matter_list.html'
    # paginate_by = 10
    queryset = RawMatter.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# class ConsumablesListView(ListView):
#     template_name = 'product/list/consumables_list.html'
#     paginate_by = 10

#     def get_queryset(self):
#         if Product.objects.all():
#             try:
#                 queryset = Product.objects.filter(category=Category.objects.get(name="pièce consommable").id)
#             except:
#                 messages.warning('test')
#         else:
#             queryset = Product.objects.none()
#         return queryset

#     @method_decorator(login_required(login_url=reverse_lazy('login')))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

# class SparePartsListView(ListView):
#     template_name = 'product/list/spare_parts_list.html'
#     paginate_by = 10

#     def get_queryset(self):
#         if Product.objects.all():
#             try:
#                 queryset = Product.objects.filter(category=Category.objects.get(name="pièce de rechange").id)
#             except:
#                 messages.warning('test')
#         else:
#             queryset = Product.objects.none()
#         return queryset

#     @method_decorator(login_required(login_url=reverse_lazy('login')))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


class CoilListView(ListView):
    template_name = 'product/list/coil_list.html'
    # paginate_by = 10
    queryset = CoilType.objects.all()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    template_name = 'product/delete/product_delete.html'
    success_url = reverse_lazy('product:index')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Product, slug=_slug)

# ##-------------------------  End Product Form ------------------------##
