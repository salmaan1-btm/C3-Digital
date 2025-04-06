from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Product, Dealership, Claim, Sale, Inventory
from .forms import SalesForm, ProductForm, ClaimsForm, SupportForm, InventoryForm
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64

# Create your views here.

@login_required
def index(request):
    claims = Claim.objects.filter(status='initiated')[:5]  # Ongoing claims
    dealerships = Dealership.objects.all()  # Show all dealerships
    sales = Sale.objects.all()[:5]  # Recent sales

    context = {
        'claims': claims,
        'dealerships': dealerships,
        'sales': sales
    }
    return render(request, 'C3_app1/index.html', context)

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

@login_required
def claim_detail_view(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)  # Fetch claim or return 404
    return render(request, 'C3_app1/claims_detail.html', {'claim': claim})

@login_required
def new_claims(request):
    """ Add a new Sales Transaction through a form."""
    if request.method != 'POST':
        #no data submitted; create a blank form.
        form = ClaimsForm()
    else:
        #POST data submitted; process data.
        form = ClaimsForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('C3_app1:claims')
    # Display a blank or invalid form.
    context = {'form' : form}
    return render(request, 'C3_app1/new_claim.html', context)

@login_required
def edit_claim(request, claim_id):

    # Get the claim instance
    claim = get_object_or_404(Claim, id=claim_id)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = ClaimsForm(instance=claim)
    else:
        # POST data submitted; process data
        form = ClaimsForm(instance=claim, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('C3_app1:claims')

    context = {'claim': claim, 'form': form}
    return render(request, 'C3_app1/edit_claim.html', context)

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
def personal_details(request):
    return render(request, 'C3_app1/personal_details.html')

@login_required
def new_sales(request):
    """ Add a new Sales Transaction through a form."""
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
    """Displays all sales transactions."""
    saleslist = Sale.objects.order_by('-date_added')
    context={'view_sales':saleslist}
    return render(request, 'C3_app1/view_sales.html',context)


@login_required
def dealership_inventory(request, dealership_id):
    """Displays products for a specific dealership."""
    dealership = Dealership.objects.get(id=dealership_id)
    inventory_items = Inventory.objects.filter(dealership=dealership)
    return render(request, 'C3_app1/dealership_inventory.html', {
        'dealership': dealership,
        'inventory_items': inventory_items
    })

@login_required
def add_inventory(request):
    if request.method != 'POST':
    #no data submitted; create a blank form.
        form = InventoryForm()
    else:
        #POST data submitted; process data.
        form = InventoryForm(data = request.POST)

        if form.is_valid():
            # Access cleaned data from the form
            product = form.cleaned_data['product']
            dealership = form.cleaned_data['dealership']
            quantity = form.cleaned_data['quantity']

            # Try to get or create the inventory entry
            inventory, created = Inventory.objects.get_or_create(
                product=product, dealership=dealership, defaults={'quantity': quantity}
            )

            if not created:
                inventory.stock += quantity  # Update the stock
                inventory.save()

        return redirect('C3_app1:inventory')
    context = {'form':form}
    return render(request, 'C3_app1/add_inventory.html', context)


@login_required
def view_products(request):
    """Displays all products offered."""
    products = Product.objects.all()
    return render(request, 'C3_app1/view_products.html', {'products':products})

@login_required
def new_product(request):
    """ Add a new product through a form."""
    if request.method != 'POST':
        #no data submitted; create a blank form.
        form = ProductForm()
    else:
        #POST data submitted; process data.
        form = ProductForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect('C3_app1:sales_p')
    # Display a blank or invalid form.
    context = {'form' : form}
    return render(request, 'C3_app1/new_product.html', context)

@login_required
def edit_product(request, product_id):
    """Allow only admin/superuser to edit the existing product"""
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to edit products.")
    """Edit an existing product"""
    product = Product.objects.get(id = product_id)
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = ProductForm(instance = product)
    else:
        #POST data submitted; prcess data.
        form = ProductForm(instance = product, data = request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect('C3_app1:view_products')
    context = {'product': product, 'form': form}
    return render(request, 'C3_app1/edit_product.html', context)


def support_view(request):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            messages.success(request, "Your request has been submitted successfully.")
            return redirect("C3_app1:support")  

    else:
        form = SupportForm()
    
    return render(request, "C3_app1/support.html", {"form": form})

def plot(request):
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]

    fig, ax = plt.subplots()
    ax.bar(x, y)

    # Optional: chart title and label axes.
    ax.set_title("Square Numbers", fontsize=24)
    ax.set_xlabel("Value", fontsize=14)
    ax.set_ylabel("Square of Value", fontsize=14)
    
    # Create a bytes buffer for saving image
    figbuffer = BytesIO()
    plt.savefig(figbuffer, format='png', dpi=300)
    image_base640=base64.b64encode(figbuffer.getvalue())
    image_base64 = image_base640.decode('utf-8')
    figbuffer.close()    
    context={'image_base64':image_base64 }
    return render(request,'C3_app1/plot.html',context)
