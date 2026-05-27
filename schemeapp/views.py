from django.shortcuts import render, redirect, get_object_or_404
from salesapp.models import Product, Sales
from .models import SchemeCustomer, SchemePayment, SchemeGoodsPickup
from django.db.models import Sum
from stockapp.models import Stock
from django.contrib import messages
from datetime import datetime
from decimal import Decimal
import re
from .validators import validate_nin,validate_phone

# from stockapp.decorators import role_required, login_required_custom

# Create your views here.

# @login_required_custom
def scheme_customer_list(request):
    customers = SchemeCustomer.objects.all().order_by("-date_registered")
    return render(request, "scheme_customer_list.html", {"customers": customers})


# @role_required('Admin', 'Staff')
def register_scheme_customer(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        nin_number = request.POST.get("nin_number", "").strip().upper()
        phone_number = request.POST.get("phone_number", "").strip()
        address = request.POST.get("address", "").strip()
        occupation = request.POST.get("occupation", "").strip()

        errors = {}

        nin_pattern = r"^(CM|CF)[0-9]{10}[A-Z]{2}$"
        phone_pattern = r"^07[0-9]{8}$"

        if not full_name:
            errors["full_name_error"] = "Full name is required."

        if not nin_number:
            errors["nin_error"] = "NIN number is required."
        elif not re.match(nin_pattern, nin_number):
            errors["nin_error"] = "Invalid NIN format. Use format like CM1234567890AB."
        elif SchemeCustomer.objects.filter(nin_number=nin_number).exists():
            errors["nin_error"] = "A customer with this NIN already exists."

        if not phone_number:
            errors["phone_error"] = "Phone number is required."
        elif not re.match(phone_pattern, phone_number):
            errors["phone_error"] = "Invalid phone number. Use format like 0781234567."

        if not address:
            errors["address_error"] = "Address is required."

        if not occupation:
            errors["occupation_error"] = "Occupation is required."

        if errors:
            return render(request, "register_scheme_customer.html", {
                "errors": errors,
                "form_data": request.POST
            })

        SchemeCustomer.objects.create(
            full_name=full_name,
            nin_number=nin_number,
            phone_number=phone_number,
            address=address,
            occupation=occupation,
        )

        messages.success(request, "Scheme customer registered successfully.")
        return redirect("scheme_customer_list")

    return render(request, "register_scheme_customer.html")

# @role_required('Admin', 'Staff', 'Cashier')
def record_scheme_payment(request, customer_id):
    customer = get_object_or_404(SchemeCustomer, id=customer_id)

    if request.method == "POST":
        payment = SchemePayment.objects.create(
            customer=customer,
            amount_paid=request.POST.get("amount_paid"),
            notes=request.POST.get("notes"),
        )

        return redirect("temporary_receipt", payment_id=payment.id)

    return render(request, "record_scheme_payment.html", {"customer": customer})


# @login_required_custom
def temporary_receipt(request, payment_id):
    payment = get_object_or_404(SchemePayment, id=payment_id)
    return render(request, "temporary_receipt.html", {"payment": payment})


# @login_required_custom
def customer_scheme_detail(request, customer_id):
    customer = get_object_or_404(SchemeCustomer, id=customer_id)
    payments = SchemePayment.objects.filter(customer=customer)
    pickups = SchemeGoodsPickup.objects.filter(customer=customer)

    total_paid = sum(payment.amount_paid for payment in payments)
    total_goods_value = sum(
        pickup.quantity_taken * pickup.product.unit_price for pickup in pickups
    )

    balance = total_paid - total_goods_value

    return render(request, "customer_scheme_details.html", {
        "customer": customer,
        "payments": payments,
        "pickups": pickups,
        "total_paid": total_paid,
        "total_goods_value": total_goods_value,
        "balance": balance,
    })


# @role_required('Admin', 'Staff', 'Cashier')

def scheme_goods_pickup(request, customer_id):

    customer = get_object_or_404(
        SchemeCustomer,
        id=customer_id
    )

    products = Product.objects.all()

    if request.method == "POST":

        product = get_object_or_404(
            Product,
            id=request.POST.get("product")
        )

        try:
            quantity = int(request.POST.get("quantity"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity")
            return render(request, "scheme_goods_pickup.html", {
                "customer": customer,
                "products": products
            })

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than 0")
            return render(request, "scheme_goods_pickup.html", {
                "customer": customer,
                "products": products
            })

        selling_price = Decimal(str(product.unit_price))
        base_total = selling_price * quantity

        distance = Decimal(request.POST.get("distance") or "0")

        if distance <= 10 and base_total >= Decimal("500000"):
            transport_cost = Decimal("0")
            transport_note = "free delivery"
        else:
            transport_cost = Decimal("30000")
            transport_note = "standard delivery fees"

        total_price = base_total + transport_cost

        sale = Sales.objects.create(
            product_name=product,
            quantity=quantity,
            total_price=total_price,
            transport_cost=transport_cost,
            transport_note=transport_note,
            distance=distance
        )

        SchemeGoodsPickup.objects.create(
            customer=customer,
            product=product,
            quantity_taken=quantity,
            linked_sale=sale
        )

        messages.success(request, "Goods pickup recorded successfully.")
        return redirect("invoice", sale_id=sale.id)

    return render(request, "scheme_goods_pickup.html", {
        "customer": customer,
        "products": products
    })

def scheme_report(request):
    sales = Sales.objects.all()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

   
    if start_date and end_date:
        sales = sales.filter(sale_date__range=[start_date, end_date])


    total_goods = sum(
        s.product_name.unit_price * s.quantity for s in sales
    )

    total_transport = sales.aggregate(
        total=Sum("transport_cost")
    )["total"] or 0

    grand_total = total_goods + total_transport

    context = {
        "sales": sales,
        "total_goods": total_goods,
        "total_transport": total_transport,
        "grand_total": grand_total,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "scheme_report.html", context)

def scheme_statement(request, customer_id):

    customer = get_object_or_404(
        SchemeCustomer,
        id = customer_id
    )

    pickups = SchemeGoodsPickup.objects.filter(
        customer=customer
    ).select_related("linked_sale", "product")

    total_goods = 0
    total_transport = 0

    for pickup in pickups:
        sale = pickup.linked_sale

        if sale:
            total_goods += sale.total_price + sale.transport_cost
            total_transport += sale.transport_cost

    grand_total = total_goods + total_transport

    context = {
        "customer": customer,
        "pickups": pickups,
        "total_goods": total_goods,
        "total_transport": total_transport,
        "grand_total": grand_total,
    }

    return render(
        request,
        "scheme_statement.html",
        context
    )