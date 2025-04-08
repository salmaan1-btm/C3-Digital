from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from .models import Product, Dealership, Claim, Sale, Inventory
from .forms import SalesForm, ProductForm, ClaimsForm, SupportForm, InventoryForm
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
import seaborn as sns

# Create your views here.

@login_required
def index(request):
    claims = Claim.objects.filter(status='initiated')[:5]  # Ongoing claims
    dealerships = Dealership.objects.all()  # Show all dealerships
    sales = Sale.objects.order_by('-id')[:5]  # Recent sales

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

def claims_delete(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)
    
    if request.method == 'POST':
        claim.delete()
        return redirect('C3_app1:claims')

def claims_chart(request):
    # Count each claim type
    submitted = Claim.objects.filter(status='submitted').count()
    initiated = Claim.objects.filter(status='initiated').count()
    rejected = Claim.objects.filter(status='rejected').count()

    labels = ['Submitted', 'Initiated', 'Rejected']
    values = [submitted, initiated, rejected]
    colors = ['#20c997', '#0ca275', '#0d7455']

    # Plot setup
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title('Claims Overview')
    plt.ylabel('Number of Claims')

    # Render to BytesIO
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')

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
def new_sales(request):
    """ Add a new Sales Transaction through a form."""
    if request.method != 'POST':
        form = SalesForm()
    else:
        form = SalesForm(data=request.POST)
        if form.is_valid():
            form.save()

            


    context = {'form': form}
    return render(request, 'C3_app1/new_sales.html', context)
   


@login_required
def view_sales(request):
    """Displays all sales transactions and renders a modern sales summary chart."""
    saleslist = Sale.objects.all().order_by('-id')

    # Aggregate quantities sold per product
    sales_summary = {}
    for sale in saleslist:
        product_name = sale.inventory.product.name
        sales_summary[product_name] = sales_summary.get(product_name, 0) + sale.quantity

    # Modern styling
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Teal color gradient (brand match)
    colors = plt.cm.cubehelix(np.linspace(0.4, 0.7, len(sales_summary)))
    bars = ax.bar(sales_summary.keys(), sales_summary.values(), color=colors, edgecolor='white', linewidth=1.5)

    # Titles & Labels
    ax.set_title("📊 Total Sales Quantity by Product", fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel("Product", fontsize=12, labelpad=10)
    ax.set_ylabel("Quantity Sold", fontsize=12, labelpad=10)
    ax.tick_params(axis='x', labelsize=10, rotation=25)
    ax.tick_params(axis='y', labelsize=10)

    # Rounded edges & annotation
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Remove clutter
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Grid styling
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5)
    ax.xaxis.grid(False)

    # Save to buffer
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=300)
    plt.close(fig)
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    context = {
        'view_sales': saleslist,
        'sales_chart': image_base64
    }

    return render(request, 'C3_app1/view_sales.html', context)


@login_required
def dealership_inventory(request, dealership_id):
    """Displays products for a specific dealership with a stock doughnut chart."""
    dealership = Dealership.objects.get(id=dealership_id)
    inventory_items = Inventory.objects.filter(dealership=dealership)

    # Prepare data for the doughnut chart
    product_names = [item.product.name for item in inventory_items]
    raw_stocks = [item.quantity for item in inventory_items]
    total_stock = sum(raw_stocks) or 1  # Avoid division by zero
    product_stocks = [round((qty / total_stock) * 100, 2) for qty in raw_stocks]
    reorder_thresholds = [item.product.reorder_threshold for item in inventory_items]

    bar_colors = [
    'rgba(0, 128, 0, 0.8)' if item.quantity > item.product.reorder_threshold  # green for sufficient
    else 'rgba(255, 0, 0, 0.8)'  # red for low stock
    for item in inventory_items
]


    context = {
        'dealership': dealership,
        'inventory_items': inventory_items,
        'product_names': product_names,
        'product_stocks': product_stocks,
        'reorder_thresholds': reorder_thresholds,
        'bar_colors': bar_colors,
    }

    return render(request, 'C3_app1/dealership_inventory.html', context)

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
                product=product,
                dealership=dealership,
                defaults={'quantity': quantity})
            
            if not created:
                inventory.quantity += quantity
                inventory.save()

            return redirect('C3_app1:dealership_inventory', dealership_id=dealership.id)

        else:
            print("Form is invalid:", form.errors)

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
            return redirect('C3_app1:view_products')
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

@login_required
def settings(request):
    """The settings page for C3 App 1."""
    return render(request, 'C3_app1/settings.html')

@login_required
def personal_details(request):
    return render(request, 'C3_app1/personal_details.html')

