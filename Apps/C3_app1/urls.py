from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'C3_app1'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('claims/', views.claims, name='claims'),
    path('claims/<int:claim_id>/', views.claim_detail_view, name='claims_detail'), 
    path('claims/<int:claim_id>/edit/', views.edit_claim, name='edit_claim'),
    path('claims/<int:claim_id>/delete/', views.claims_delete, name='claims_delete'),
    path('new_claim/', views.new_claims, name='new_claim'),
    path('claims/chart/', views.claims_chart, name='claims_chart'),
    path('inventory/', views.inventory, name='inventory'),
    path('add_inventory/', views.add_inventory, name = 'add_inventory'),
    path('sales_p/', views.sales_p, name='sales_p'),
    path('settings/', views.settings, name='settings'),
    path('details/', views.personal_details, name='personal_details'),
    path('view_sales/', views.view_sales, name='view_sales'),
    path('sales_chart/', views.sales_chart, name='sales_chart'),
    path('new_sales/', views.new_sales, name = 'new_sales'),
    path('view_products/', views.view_products, name = 'view_products'),
    path('new_product/', views.new_product, name = 'new_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name = 'edit_product'),
    path('inventory/dealership/<int:dealership_id>/', views.dealership_inventory, name='dealership_inventory'),
    path("support/", views.support_view, name="support"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='C3_app1/password_change.html',success_url=reverse_lazy('C3_app1:password_change_done')),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='C3_app1/password_change_done.html'), name='password_change_done'),
    
]
