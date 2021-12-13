from django.urls import path, include
from .views import *

app_name = 'product'

urlpatterns = [
     # Main View
     path('', ProductIndexView.as_view(), name='index'),
     # Brands Url Management
     path('brand/list/', BrandListView.as_view(), name='brands'),
     path('brand/create/', BrandCreateView.as_view(), name='brand-create'),
     path('brand/<slug>/update/', BrandUpdateView.as_view(), name='brand-update'),
     path('brand/<slug>/delete/', BrandDeleteView.as_view(), name='brand-delete'),

     # Ranges Url Management
     path('product/range/list/', RangeListView.as_view(), name='ranges'),
     path('product/range/create/', RangeCreateView.as_view(), name='range-create'),
     path('product/range/<slug>/update/', RangeUpdateView.as_view(), name='range-update'),
     path('product/range/<slug>/delete/',RangeDeleteView.as_view(), name='range-delete'),

     # CombinedRanges Url Management
     path('product/c-range/list/', CombinedRangeListView.as_view(), name='c-ranges'),
     path('product/c-range/create/', CombinedRangeCreateView.as_view(), name='c-range-create'),
     path('product/c-range/<slug>/update/', CombinedRangeUpdateView.as_view(), name='c-range-update'),
     path('product/c-range/<slug>/delete/', CombinedRangeDeleteView.as_view(), name='c-range-delete'),

     # Colors Url Management
     path('color/list/', ColorListView.as_view(), name='colors'),
     path('color/create/', ColorCreateView.as_view(), name='color-create'),
     path('color/<slug>/update/', ColorUpdateView.as_view(), name='color-update'),
     path('color/<slug>/delete/', ColorDeleteView.as_view(), name='color-delete'),

     # Flavors Url Management
     path('flavor/list/', FlavorListView.as_view(), name='flavors'),
     path('flavor/create/', FlavorCreateView.as_view(), name='flavor-create'),
     path('flavor/<slug>/update/', FlavorUpdateView.as_view(), name='flavor-update'),
     path('flavor/<slug>/delete/', FlavorDeleteView.as_view(), name='flavor-delete'),

     # ### Consumables Url Managemnt
     path('consumable/index-consumables/', IndexConsumablesView.as_view(), name='index-consumables'),

     path('handle/create/handle-create/',HandleCreateView.as_view(), name='handle-create'),
     path('handle/update/handle-update/<slug>/',HandleUpdateView.as_view(), name='handle-update'),
     path('handle/list/handle/', HandleListView.as_view(), name='handles'),
     path('handle/delete/handle-delete/<slug>/', HandleDeleteView.as_view(), name='handle-delete'),


     path('labelling/create/labelling-create/',LabellingCreateView.as_view(), name='labelling-create'),
     path('labelling/update/labelling-update/<slug>/',LabellingUpdateView.as_view(), name='labelling-update'),
     path('labelling/list/labelling/', LabellingListView.as_view(), name='labellings'),
     path('labelling/delete/labelling-delete/<slug>/', LabellingDeleteView.as_view(), name='labelling-delete'),

     path('labelling/create/package-create/',PackageCreateView.as_view(), name='package-create'),
     path('labelling/update/package-update/<slug>/',PackageUpdateView.as_view(), name='package-update'),
     path('labelling/list/package/', PackageListView.as_view(), name='packages'),
     path('labelling/delete/package-delete/<slug>/', PackageDeleteView.as_view(), name='package-delete'),

     path('tape/create/tape-create/',TapeCreateView.as_view(), name='tape-create'),
     path('tape/update/tape-update/<slug>/',TapeUpdateView.as_view(), name='tape-update'),
     path('tape/list/tape/', TapeListView.as_view(), name='tapes'),
     path('tape/delete/tape-delete/<slug>/', TapeDeleteView.as_view(), name='tape-delete'),

     path('spare-part/create/part-create/',PartCreateView.as_view(), name='part-create'),
     path('spare-part/update/part-update/<ref>/',PartUpdateView.as_view(), name='part-update'),
     path('spare-part/list/part/', PartListView.as_view(), name='parts'),
     path('spare-part/delete/part-delete/<ref>/', PartDeleteView.as_view(), name='part-delete'),

     # # Product List Url
     path('product/list/final-product/',FinalProductListView.as_view(), name='products'),
     path('product/list/raw-matter/',RawMatterListView.as_view(), name='rawmatters'),
     path('product/list/coils/', CoilListView.as_view(), name='coils'),

     # # Product Creation Url
     path('product/create/raw-matter/',RawMatterCreateView.as_view(), name='raw-matter-create'),
     path('product/create/coil/', CoilCreateView.as_view(), name='coil-create'),
     path('product/create/final-product/',FinalProductCreateView.as_view(), name='final-product-create'),

     # # Product Update Url
     path('product/coil/<slug>/update/',CoilUpdateView.as_view(), name='coil-update'),
     path('product/raw-matter/<slug>/update/',RawMatterUpdateView.as_view(), name='raw-matter-update'),
     path('product/final-product/<slug>/update/',FinalProductUpdateView.as_view(), name='final-product-update'),

     # # Product Delete Url
     path('product/<slug>/delete/',ProductDeleteView.as_view(), name='product-delete'),

]
