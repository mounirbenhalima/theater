from django.urls import path, include
from .views import (
    raw_matter_entry,
    raw_matter_out,
    final_product_entry,
    final_product_out,
    final_product_return,
    CoilEntryView,
    CoilsListView,
    entry_coil_list,
    IndexView,
    HandleIndexView,
    TapeIndexView,
    LabellingIndexView,
    PackageIndexView,
    add_to_cart,
    OrderSummaryView,
    validate_order,
    delete_order,
    EntryStockList,
    remove_from_cart,
    email,
    stock_movement,
    trashout_invoice,
    OrderList,
    OrderDetail,
    stock_status,
    FinishedProductListView,
    trash_validation,
    GeneralTrashCreateView,
    TrashOutView,
    TrashInRecapView,
    TrashOutRecapView,
    RecapPage,
    recap,
    RawMatterIndexView,
    ConsumablesIndexView,
    SparePartIndexView,
    SparePartConsumptionView,
    CoilsIndexView,
    CoilSale,
    FinishedProductIndexView,
    TrashIndexView,
    ControlIndexView,
    QuarantineCoilListView,
    destroy_coil,
    delete_final_product,
    difference_rawmatter_workshop,
    stock_workshop_status,
    rawmatter_loss,
    workshop_rawmatter_loss,
    labelling_loss,
    workshop_labelling_loss,
    package_loss,
    workshop_package_loss,
    handle_entry,
    handle_out,
    labelling_entry,
    labelling_out,
    package_entry,
    package_out,
    tape_entry,
    part_entry,
    part_out,
    tape_out,
    difference_package_workshop,
    difference_labelling_workshop,
    difference_handle_workshop,

)

app_name = 'stock-manager'


urlpatterns = [

    path('stock-manager-rawmatter/', RawMatterIndexView.as_view(), name='index-raw-matter'),
    path('stock-manager-finished-product/', FinishedProductIndexView.as_view(), name='index-finished-product'),
    path('stock-manager-delete-final-product-production/<slug>/', delete_final_product, name='delete-final-product-production'),
    path('stock-manager-consumables/', ConsumablesIndexView.as_view(), name='index-consumables'),
    path('stock-manager-exchange-parts/', SparePartIndexView.as_view(), name='index-exchange-parts'),
    path('stock-manager-coils/', CoilsIndexView.as_view(), name='index-coils'),
    path('stock-manager-trash/', TrashIndexView.as_view(), name='index-trash'),
    path('stock-manager-control/', ControlIndexView.as_view(), name='index-control'),



    # Trash
    path('stock-entry/trash/', trash_validation, name="trash-validation"),
    path('stock-entry/trash-entry/', GeneralTrashCreateView.as_view(), name="general-trash"),
    path('stock-entry/trash-out/', TrashOutView.as_view(), name="trash-out"),
    path('stock-entry/trash-in-recap/', TrashInRecapView.as_view(), name="trash-in-recap"),
    path('stock-entry/trash-out-recap/', TrashOutRecapView.as_view(), name="trash-out-recap"),

    # Raw Matter
    path('stock-entry/raw-matter/', raw_matter_entry, name="raw-matter-entry"),
    path('stock-out/raw-matter/', raw_matter_out, name="raw-matter-out"),
    path('stock-return/raw-matter/', raw_matter_entry, name="raw-matter-return"),
    path('stock-status/raw-matter/', raw_matter_entry, name="raw-matter-status"),
    path('stock-status/rawmatter-workshop/', difference_rawmatter_workshop, name="rawmatter-workshop"),
    path('stock-status/rawmatter-loss/', rawmatter_loss, name="rawmatter-loss"),
    path('stock-status/workshop-rawmatter-loss/', workshop_rawmatter_loss, name="workshop-rawmatter-loss"),
    

    # Handle
    path('stock-entry/handle-index/', HandleIndexView.as_view(), name="handle-index"),
    path('stock-entry/handle-entry/', handle_entry, name="handle-entry"),
    path('stock-out/handle-out/', handle_out, name="handle-out"),
    path('stock-status/handle-workshop/', difference_handle_workshop, name="handle-workshop"),
    

    # Tape
    path('stock-entry/tape-index/', TapeIndexView.as_view(), name="tape-index"),
    path('stock-entry/tape-entry/', tape_entry, name="tape-entry"),
    path('stock-out/tape-out/', tape_out, name="tape-out"),

    # Labelling
    path('stock-entry/labelling-index/', LabellingIndexView.as_view(), name="labelling-index"),
    path('stock-entry/labelling-entry/', labelling_entry, name="labelling-entry"),
    path('stock-out/labelling-out/', labelling_out, name="labelling-out"),
    path('stock-status/labelling-workshop/', difference_labelling_workshop, name="labelling-workshop"),
    path('stock-status/labelling-loss/', labelling_loss, name="labelling-loss"),
    path('stock-status/workshop-labelling-loss/', workshop_labelling_loss, name="workshop-labelling-loss"),

    # Spare Part
    path('stock-entry/part-index/', SparePartIndexView.as_view(), name="part-index"),
    path('stock-entry/part-entry/', part_entry, name="part-entry"),
    path('stock-out/part-out/', part_out, name="part-out"),
    path('stock-out/part-consumption/', SparePartConsumptionView.as_view(), name='part-consumption'),
    # path('stock-status/labelling-workshop/', difference_labelling_workshop, name="labelling-workshop"),
    # path('stock-status/labelling-loss/', labelling_loss, name="labelling-loss"),
    # path('stock-status/workshop-labelling-loss/', workshop_labelling_loss, name="workshop-labelling-loss"),

    # Package
    path('stock-entry/package-index/', PackageIndexView.as_view(), name="package-index"),
    path('stock-entry/package-entry/', package_entry, name="package-entry"),
    path('stock-out/package-out/', package_out, name="package-out"),
    path('stock-status/package-workshop/', difference_package_workshop, name="package-workshop"),
    path('stock-status/package-loss/', package_loss, name="package-loss"),
    path('stock-status/workshop-package-loss/', workshop_package_loss, name="workshop-package-loss"),

    # # Final Produt
    path('stock-out/final-product/', final_product_out, name="final-product-out"),
    path('stock-return/final-product/', final_product_return, name="final-product-return"),
    path('stock-entry/final-product/', final_product_entry, name="final-product-entry"),

    # # Coil
    path('stock-entry/coil/', CoilEntryView.as_view(), name="coil-entry"),
    path('entry-coil-list/', entry_coil_list, name='entry-coil-list'),
    path('stock-out/coil/', CoilsListView.as_view(), name="detail-coils"),
    path('stock-return/coil/', CoilEntryView.as_view(), name="coil-return"),
    path('stock-status/coil/', CoilEntryView.as_view(), name="coil-status"),
    path('quarantine-coil/', QuarantineCoilListView.as_view(), name='quarantine-coil'),
    path('destroy-coil/<slug>/', destroy_coil, name='destroy-coil'),
    path('coil-sale/', CoilSale.as_view(), name='coil-sale'),
    

    # ## ##
    path('', IndexView.as_view(), name='index'),
    path('add-to-order/<slug>/', add_to_cart, name="add-to-order"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('order-validation/', validate_order, name="order-validation"),
    path('order-delete/<slug>/', delete_order, name="order-delete"),
    path('orders-entry/', EntryStockList.as_view(), name="orders-entry"),
    path('remove-item/<identifier>/', remove_from_cart, name="remove-item"),
    path('orders-list/', OrderList.as_view(), name="orders-list"),
    path('stock-invoice/<slug>/', stock_movement, name="invoice"),
    path('order-detail/<slug>/', OrderDetail.as_view(), name="order-detail"),

    path('inventory/<category>/', stock_status, name="stock-status"),
    path('inventory-workshop/<category>/', stock_workshop_status, name="stock-workshop-status"),

    path('trashout-invoice/<ref>/', trashout_invoice, name='trashout-invoice'),

    path('recap-page/', RecapPage.as_view(), name='recap-page'),
    path(r'^recap/search/', recap, name='recap'),
    # Mail TEst
    path('send-mail/', email),
    #     path('reportlab/<slug>/', pdf_generation, name="order_ssy"),
]
