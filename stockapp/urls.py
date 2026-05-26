
from django.contrib import admin
from django.urls import path, include
from stockapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.stock_list, name='stock_list'),
    path('create_receipt/', views.create_receipt, name='create_receipt'),
    path('receipt/<int:receipt_id>/', views.goods_received_note, name='goods_received_note'),
    path('stock_edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('delete_receipt/<int:receipt_id>/', views.delete_receipt, name='delete_receipt'),
    path('stock_report/', views.stock_report, name='stock_report'),
]