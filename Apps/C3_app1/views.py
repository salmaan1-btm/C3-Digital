from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """The home page for C3 App 1."""
    return render(request, 'C3_app1/index.html')

@login_required
def claims(request):
    """The Claims page for C3 App 1."""
    return render(request, 'C3_app1/claims.html')

@login_required
def inventory(request):
    """The inventory page for C3 App 1."""
    return render(request, 'C3_app1/inventory.html')

@login_required
def sales_p(request):
    """The sales portal page for C3 App 1."""
    return render(request, 'C3_app1/sales_p.html')

