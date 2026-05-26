from django.urls import path
from . import views


urlpatterns = [
    path("", views.scheme_customer_list, name="scheme_customer_list"),
    path("register/", views.register_scheme_customer, name="register_scheme_customer"),
    path("customer/<int:customer_id>/", views.customer_scheme_detail, name="customer_scheme_detail"),
    path("customer/<int:customer_id>/payment/", views.record_scheme_payment, name="record_scheme_payment"),
    path("payment/<int:payment_id>/receipt/", views.temporary_receipt, name="temporary_receipt"),
    path("customer/<int:customer_id>/pickup/", views.scheme_goods_pickup, name="scheme_goods_pickup"),
    path("scheme/customers/", views.scheme_customer_list, name="scheme_customer_list"),
    path("scheme/report", views.scheme_report, name="scheme_report"),
    path('scheme/customer/statement/<int:customer_id>/',views.scheme_statement,name='scheme_statement')
]