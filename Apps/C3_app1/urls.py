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
    path('new_sales/', views.new_sales, name = 'new_sales'),
]
