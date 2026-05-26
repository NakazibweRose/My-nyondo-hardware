from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Stock
from salesapp.models import Product

# Stock list
def stock_list(request):
    stocks = Stock.objects.all().order_by("-date")
    return render(request, 'stock_list.html', {'stocks': stocks})

# Create receipt
def create_receipt(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product = get_object_or_404(Product, id=request.POST.get('product'))
        unit_cost = float(request.POST.get('unit_cost') or 0)
        amount_paid = float(request.POST.get('amount_paid') or 0)
        receipt = Stock.objects.create(
            product=product,
            supplier=request.POST.get('supplier'),
            quantity=int(request.POST.get('quantity')),
            unit_cost=unit_cost,
            amount_paid=amount_paid,
            selling_price =float(request.POST.get('price') or 0),
            date=request.POST.get('date'),
            is_paid= request.POST.get('is_paid') == 'on'
        )
        return redirect('goods_received_note', receipt_id=receipt.id)

    # products = Product.objects.all()
    return render(request, 'create_receipt.html', context={'products': products})

# Goods received note
def goods_received_note(request, receipt_id):
    receipt = get_object_or_404(Stock, id=receipt_id)
    total_amount_due = receipt.quantity * receipt.unit_cost
    return render(request, 'goods_received_note.html', context={'receipt': receipt, 'total_amount_due': total_amount_due})

# Edit receipt
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)

    if request.method == "POST":
        stock.product = request.POST.get("product")
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
    products = Stock.objects.all()
    report = []
    for product in products:
        total_stock = Stock.objects.filter(
            product=product.product
        ).aggregate(total=Sum('quantity'))['total'] or 0

        total_sold = 0  # Replace with actual sales data if available

        current_stock = total_stock - total_sold

        if current_stock < 10:
            status = 'Low Stock'
        elif current_stock < 50:
            status = 'Medium Stock'
        else:
            status = 'High Stock'

        report.append((
            product.product,  # fixed field name
            total_stock,
            total_sold,
            current_stock,
            status
        ))

    return render(request, 'stock_report.html', context={'report': report})

