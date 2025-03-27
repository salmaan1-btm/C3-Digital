from django.urls import path
from . import views

app_name = 'C3_app1'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('claims/', views.claims, name='claims'),
    path('claims/<int:claim_id>/', views.claim_detail_view, name='claims_detail'), 
    path('inventory/', views.inventory, name='inventory'),
    path('sales_p/', views.sales_p, name='sales_p'),
    path('settings/', views.settings, name='settings'),
    path('view_sales/', views.view_sales, name='view_sales'),
    path('new_sales/', views.new_sales, name = 'new_sales'),
    path('view_products/', views.view_products, name = 'view_products'),
    path('new_product/', views.new_product, name = 'new_product'),
    path('inventory/dealership/<int:dealership_id>/', views.dealership_inventory, name='dealership_inventory'),
]
