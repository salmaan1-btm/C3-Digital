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
from collections import defaultdict
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

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
    colors = ['#a0d9d5','#20c997', '#f7c6c7']

    # Plot setup
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title('Claims Overview')
    plt.ylabel('Number of Claims', fontsize=12, labelpad=16)

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
            return redirect('C3_app1:view_sales')

            


    context = {'form': form}
    return render(request, 'C3_app1/new_sales.html', context)
   


@login_required
def view_sales(request):
    """Displays all sales transactions."""
    saleslist = Sale.objects.all().order_by('-id')
    context={'view_sales':saleslist}
    return render(request, 'C3_app1/view_sales.html',context)

@login_required
def sales_chart(request):
    from .models import Sale

    # Gather total sales quantity per product
    product_sales = {}
    for sale in Sale.objects.select_related('inventory__product'):
        product_name = sale.inventory.product.name
        product_sales[product_name] = product_sales.get(product_name, 0) + sale.quantity

    if not product_sales:
        return HttpResponse("No sales data available", content_type="text/plain")

    labels = list(product_sales.keys())
    values = list(product_sales.values())
    colors = sns.color_palette("pastel", len(labels))

    # Generate the bar chart
    plt.figure(figsize=(9, 5))
    sns.barplot(x=labels, y=values, palette=colors)
    plt.xticks(rotation=0, ha="center")
    plt.title("Total Products Sold")
    plt.ylabel("Quantity Sold" , fontsize=12, labelpad=16)
    #plt.xlabel("Product")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')





@login_required
def inventory_distribution_chart(request):
    from matplotlib.patches import Patch
    dealerships = Dealership.objects.all()
    inventory_data = Inventory.objects.select_related('dealership')

    # Aggregate inventory totals by dealership
    totals = {}
    for item in inventory_data:
        name = item.dealership.name
        totals[name] = totals.get(name, 0) + item.quantity

    if not totals:
        return HttpResponse("No inventory data available", content_type="text/plain")

    labels = list(totals.keys())
    values = list(totals.values())
    colors = sns.color_palette("pastel", len(labels))

    # Create pie chart
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        values,
        labels=None,  # Remove labels from the pie itself
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )

    # Create custom legend patches
    legend_elements = [Patch(facecolor=colors[i], label=f"{labels[i]}") for i in range(len(labels))]
    plt.legend(handles=legend_elements, title="Dealerships", loc='center left', bbox_to_anchor=(1, 0.5))

    #plt.title("Inventory Distribution by Dealership")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')  # Ensure legend doesn't get cut off
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')





@login_required
def daily_revenue_chart(request):
    from collections import defaultdict
    from datetime import timedelta
    from .models import Sale
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    from io import BytesIO

    try:
        sales = list(Sale.objects.select_related('inventory__product').order_by('date_added'))

        if not sales:
            return HttpResponse("No sales data available", content_type="text/plain")

        # Prepare revenue data by day
        revenue_by_day = defaultdict(float)
        for sale in sales:
            date = sale.date_added
            revenue = sale.quantity * float(sale.inventory.product.price)
            revenue_by_day[date] += revenue

        sorted_dates = sorted(revenue_by_day.keys())
        total_days = (sorted_dates[-1] - sorted_dates[0]).days + 1

        # Dynamic grouping logic
        if total_days <= 10:
            labels = sorted_dates
            revenues = [revenue_by_day[day] for day in labels]
            label_format = "%Y-%m-%d"
            title = "Daily Revenue"
        elif total_days <= 30:
            weekly_revenue = defaultdict(float)
            for date, rev in revenue_by_day.items():
                week_start = date - timedelta(days=date.weekday())
                weekly_revenue[week_start] += rev
            labels = sorted(weekly_revenue.keys())
            revenues = [weekly_revenue[week] for week in labels]
            label_format = "Week of %b %d"
            title = "Weekly Revenue"
        else:
            monthly_revenue = defaultdict(float)
            for date, rev in revenue_by_day.items():
                month_key = date.replace(day=1)
                monthly_revenue[month_key] += rev
            labels = sorted(monthly_revenue.keys())
            revenues = [monthly_revenue[month] for month in labels]
            label_format = "%b %Y"
            title = "Monthly Revenue"

        # Plot the chart
        plt.figure(figsize=(10, 4))
        plt.plot(labels, revenues, marker='o', linestyle='-', color="#20c997", linewidth=2)
        plt.title(title, fontsize=14)
        plt.xlabel(" ", fontsize=12, labelpad = 10)
        plt.ylabel("Revenue ($)", fontsize=14, labelpad = 20)
        plt.grid(True, linestyle='--', alpha=0.5)

        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10, prune='both'))
        ax.set_xticks(labels)
        ax.set_xticklabels([label.strftime(label_format) for label in labels], rotation=0)

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type='image/png')

    except Exception as e:
        return HttpResponse(f"An error occurred while generating the chart: {str(e)}", content_type="text/plain")








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
def dealership_inventory_chart(request, dealership_id):
    dealership = get_object_or_404(Dealership, id=dealership_id)
    inventory_items = Inventory.objects.filter(dealership=dealership).select_related('product')

    if not inventory_items:
        return HttpResponse("No inventory data available", content_type="text/plain")

    labels = []
    values = []
    bar_colors = []

    for item in inventory_items:
        labels.append(item.product.name)
        values.append(item.quantity)
        if item.quantity < item.product.reorder_threshold:
            bar_colors.append('#f7c6c7')  # pastel pink
        else:
            bar_colors.append('#a0d9d5')  # pastel teal

    plt.figure(figsize=(8, 4))
    sns.barplot(x=labels, y=values, palette=bar_colors)
    plt.xticks(rotation=0, ha='center')
    
    plt.ylabel('Stock Level', fontsize=12, labelpad=16)
    #plt.xlabel('Product', fontsize=12, labelpad=16)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')




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

