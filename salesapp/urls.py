from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.create_category, name="create_category"),
    path("categories/<int:category_id>/delete/", views.delete_category, name="delete_category"),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("products/<int:product_id>/delete/", views.delete_product, name="delete_product"),

    path("sales/create/", views.create_sale, name="create_sale"),
    path("sales/<int:sale_id>/invoice/", views.invoice, name="invoice"),
    path("sales/<int:sale_id>/edit/", views.edit_sale, name="edit_sale"),
    path("sales/<int:sale_id>/delete/", views.delete_sale, name="delete_sale"),
    path("sales/report/", views.sales_report, name="sales_report"),
    path("sales/report/export/", views.export_sales_report_excel, name="export_sales_report_excel"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
