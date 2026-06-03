from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Stock
from salesapp.models import Product, Sales
from decimal import Decimal, InvalidOperation
from django.contrib import messages

# Stock list
def stock_list(request):
    stocks = Stock.objects.all().order_by("-date")
    return render(request, 'stock_list.html', {'stocks': stocks})

# Create receipt

def create_receipt(request):
    products = Product.objects.all()

    if request.method == "POST":

        errors = {}

        product_name = request.POST.get("product")
        supplier = request.POST.get("supplier")
        quantity = request.POST.get("quantity")
        unit_cost = request.POST.get("unit_cost")
        selling_price = request.POST.get("price")
        amount_paid = request.POST.get("amount_paid")
        date = request.POST.get("date")

        # PRODUCT
        if not product_name:
            errors["product"] = "Please select a product."

        # SUPPLIER
        if not supplier:
            errors["supplier"] = "Supplier is required."

        # QUANTITY
        if not quantity:
            errors["quantity"] = "Quantity is required."
        else:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    errors["quantity"] = "Quantity must be greater than zero."
            except:
                errors["quantity"] = "Enter a valid quantity."

        # UNIT COST
        if not unit_cost:
            errors["unit_cost"] = "Unit cost is required."
        else:
            try:
                unit_cost = Decimal(unit_cost)
                if unit_cost <= 0:
                    errors["unit_cost"] = "Unit cost must be greater than zero."
            except:
                errors["unit_cost"] = "Enter a valid unit cost."

        # SELLING PRICE
        if not selling_price:
            errors["price"] = "Selling price is required."
        else:
            try:
                selling_price = Decimal(selling_price)
                if selling_price <= 0:
                    errors["price"] = "Selling price must be greater than zero."
            except:
                errors["price"] = "Enter a valid selling price."

        # AMOUNT PAID
        if not amount_paid:
            errors["amount_paid"] = "Amount paid is required."
        else:
            try:
                amount_paid = Decimal(amount_paid)
                if amount_paid < 0:
                    errors["amount_paid"] = "Amount paid cannot be negative."
            except:
                errors["amount_paid"] = "Enter a valid amount."

        # DATE
        if not date:
            errors["date"] = "Date is required."

        # STOP IF ERRORS
        if errors:
            return render(request, "create_receipt.html", {
                "products": products,
                "errors": errors
            })

        # GET PRODUCT WITHOUT ID
        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            return render(request, "create_receipt.html", {
                "products": products,
                "errors": {"product": "Selected product does not exist."}
            })

        # CREATE STOCK
        receipt = Stock.objects.create(
            product=product,
            supplier=supplier,
            quantity=quantity,
            unit_cost=unit_cost,
            selling_price=selling_price,
            amount_paid=amount_paid,
            date=date,
            is_paid=request.POST.get("is_paid") == "on"
        )

        # UPDATE PRODUCT PRICES
        product.unit_price = unit_cost
        product.selling_price = selling_price
        product.save()

        return redirect("goods_received_note", receipt_id=receipt.id)

    return render(request, "create_receipt.html", {
        "products": products
    })
# Goods received note
def goods_received_note(request, receipt_id):
    receipt = get_object_or_404(Stock, id=receipt_id)
    total_amount_due = receipt.quantity * receipt.unit_cost
    return render(request, 'goods_received_note.html', context={'receipt': receipt, 'total_amount_due': total_amount_due})

# Edit receipt
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)

    if request.method == "POST":
        product = get_object_or_404(Product, product_name=request.POST.get('product'))
        stock.product = product
        stock.supplier = request.POST.get("supplier")
        stock.quantity = int(request.POST.get("quantity") or 0)
        stock.unit_cost = float(request.POST.get("unit_cost") or 0)
        stock.amount_paid = float(request.POST.get("amount_paid") or 0)
        stock.selling_price = float(request.POST.get("price") or 0)
        stock.is_paid = bool(request.POST.get("is_paid"))

        stock.save()
        return redirect("stock_list")

    return render(request, "stock_edit.html", {
        "stock": stock
    })

# Delete receipt
def delete_receipt(request, receipt_id):
    receipt = get_object_or_404(Stock, id=receipt_id)
    if request.method == 'POST':
        receipt.delete()
        return redirect('stock_list')
    return render(request, 'delete_receipt.html', context={'receipt': receipt})

# Stock report
def stock_report(request):
    products = Product.objects.all()

    report = []

    for product in products:
        total_received = Stock.objects.filter(
            product=product
        ).aggregate(total=Sum("quantity"))["total"] or 0

        total_sold = Sales.objects.filter(
            product_name=product
        ).aggregate(total=Sum("quantity"))["total"] or 0

        current_stock = total_received - total_sold

        if current_stock < 10:
            status = "Low Stock"
        elif current_stock < 50:
            status = "Medium Stock"
        else:
            status = "High Stock"

        report.append({
            "product": product,
            "total_received": total_received,
            "total_sold": total_sold,
            "current_stock": current_stock,
            "status": status,
        })

    return render(request, "stock_report.html", {
        "report": report
    })