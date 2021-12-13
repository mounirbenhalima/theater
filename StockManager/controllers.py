from django.shortcuts import redirect


def order_redirect(order_name, order_type, order_user, request_user):
    if order_user == request_user and request_user.profile.job_position.name == 'Gestionnaire de Stock':
        if order_name == "finishedproducttype" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:final-product-entry")
        elif order_name == "finishedproducttype" and order_type == "STOCK_OUT":
            return redirect("stock-manager:final-product-out")
        elif order_name == "finishedproducttype" and order_type == "STOCK_RETURN":
            return redirect("stock-manager:final-product-return")
        elif order_name == "rawmatter" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:raw-matter-entry")
        elif order_name == "rawmatter" and order_type == "STOCK_OUT":
            return redirect("stock-manager:raw-matter-out")
        elif order_name == "rawmatter" and order_type == "STOCK_RETURN":
            return redirect("stock-manager:raw-matter-return")
        elif order_name == "coiltype" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:coil-entry")
        elif order_name == "coiltype" and order_type == "STOCK_OUT":
            return redirect("stock-manager:coil-out")
        elif order_name == "coiltype" and order_type == "STOCK_RETURN":
            return redirect("stock-manager:coil-return")
        elif order_name == "handle" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:handle-entry")
        elif order_name == "handle" and order_type == "STOCK_OUT":
            return redirect("stock-manager:handle-out")
        elif order_name == "labelling" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:labelling-entry")
        elif order_name == "labelling" and order_type == "STOCK_OUT":
            return redirect("stock-manager:labelling-out")
        elif order_name == "package" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:package-entry")
        elif order_name == "package" and order_type == "STOCK_OUT":
            return redirect("stock-manager:package-out")
        elif order_name == "tape" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:tape-entry")
        elif order_name == "tape" and order_type == "STOCK_OUT":
            return redirect("stock-manager:tape-out")
        elif order_name == "part" and order_type == "STOCK_ENTRY":
            return redirect("stock-manager:part-entry")
        elif order_name == "part" and order_type == "STOCK_OUT":
            return redirect("stock-manager:part-out")
        
    if order_user == request_user and request_user.profile.job_position.name == 'Mélangeur':
        return redirect("production:mixing-process")
