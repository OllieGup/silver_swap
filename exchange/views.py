from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Listing
from .forms import CreateListingForm 
from .models import Listing, Item
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# If you have models, import them here:
# from .models import Listing, Activity, Holding

def home(request): 
    return render(request, "home.html")

def dashboard_view(request):
    # Placeholder data — replace with real services/models later
    spot_price = 18.42
    change_amount = 0.27
    change_percent = 1.49
    premium_index = 7.2

    # Example placeholders for listings, holdings, activity
    recent_listings = []
    holdings = {
        "total_ounces": 0,
        "current_value": 0,
        "cost_basis": 0,
        "unrealised_gain": 0,
        
    }
    activity = []

    context = {
        "spot_price": spot_price,
        "change_amount": change_amount,
        "change_percent": change_percent,
        "premium_index": premium_index,
        "updated_at": timezone.now(),

        "recent_listings": recent_listings,
        "holdings": holdings,
        "activity": activity,
    }

    return render(request, "dashboard/dashboard.html", context)

def marketplace_index(request):
    listings = Listing.objects.filter(status="active").order_by("-created_at")
    context = {
        "listings": listings
    } 
    return render(request, "exchange/marketplace_index.html", context)


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'exchange/my_listings.html', {'listings': listings})
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "exchange/listing_detail.html", {"listing": listing})
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing_type = form.cleaned_data["listing_type"]

            if listing_type == "item_for_silver":
                item = Item.objects.create(
                    owner=request.user,
                    name=form.cleaned_data["item_name"],
                    description=form.cleaned_data["item_description"],
                )

                Listing.objects.create(
                    owner=request.user,
                    listing_type="item_for_silver",
                    item=item,
                    desired_silver_oz=form.cleaned_data["desired_silver_oz"],
                )

            elif listing_type == "silver_for_item":
                Listing.objects.create(
                    owner=request.user,
                    listing_type="silver_for_item",
                    bullion_amount_oz=form.cleaned_data["bullion_amount_oz"],
                    desired_item_description=form.cleaned_data["desired_item_description"],
                )

            return redirect("marketplace_index")

    else:
        form = CreateListingForm()

    return render(request, "exchange/create_listing.html", {"form": form})


def signup(request): 
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("login") 
    else: 
        form = UserCreationForm() 
    return render(request, "registration/signup.html", {"form": form})











    
