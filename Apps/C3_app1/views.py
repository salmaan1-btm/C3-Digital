from django.shortcuts import render

# Create your views here.
def index(request):
    """The home page for C3 App 1."""
    return render(request, 'C3_app1/index.html')

def claims(request):
    """The Claims page for C3 App 1."""
    return render(request, 'C3_app1/claims.html')

def inventory(request):
    """The inventory page for C3 App 1."""
    return render(request, 'C3_app1/inventory.html')

def sales_p(request):
    """The sales portal page for C3 App 1."""
    return render(request, 'C3_app1/sales_p.html')