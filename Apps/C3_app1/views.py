from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Dealership
from .sales_form import SalesForm
from .models import Claim
from .models import Sale


# Create your views here.

@login_required
def index(request):
    """The home page for C3 App 1."""
    return render(request, 'C3_app1/index.html')

@login_required
def claims(request):
    # Fetch claims by their status
    submitted_claims = Claim.objects.filter(status='submitted')
    initiated_claims = Claim.objects.filter(status='initiated')
    rejected_claims = Claim.objects.filter(status='rejected')

    # Pass them to the template
    return render(request, 'C3_app1/claims.html', {
        'submitted_claims': submitted_claims,
        'initiated_claims': initiated_claims,
        'rejected_claims': rejected_claims,
    })

def claim_detail_view(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)  # Fetch claim or return 404
    return render(request, 'C3_app1/claims_detail.html', {'claim': claim})

@login_required
def inventory(request):
    """Display dealership cards instead of full product list."""
    dealerships = Dealership.objects.all()
    return render(request, 'C3_app1/inventory.html', {'dealerships': dealerships})

@login_required
def sales_p(request):
    """The sales portal page for C3 App 1."""
    return render(request, 'C3_app1/sales_p.html')

@login_required
def settings(request):
    """The settings page for C3 App 1."""
    return render(request, 'C3_app1/settings.html')

@login_required
def new_sales(request):
    """ Add a new Sales Transaction"""
    if request.method != 'POST':
        #no data submitted; create a blank form.
        form = SalesForm()
    else:
        #POST data submitted; process data.
        form = SalesForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('C3_app1:sales_p')
    # Display a blank or invalid form.
    context = {'form' : form}
    return render(request, 'C3_app1/new_sales.html', context)

@login_required
def view_sales(request):
    """shows all sales transactions"""
    saleslist = Sale.objects.order_by('-date_added')
    context={'view_sales':saleslist}
    return render(request, 'C3_app1/view_sales.html',context)


@login_required
def dealership_inventory(request, dealership_id):
    """Displays products for a specific dealership."""
    dealership = get_object_or_404(Dealership, id=dealership_id)
    products = Product.objects.filter(dealership=dealership)
    return render(request, 'C3_app1/dealership_inventory.html', {
        'dealership': dealership,
        'products': products
    })