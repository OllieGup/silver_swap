from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Listing
from .forms import CreateListingForm 
from .models import Listing, Item
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Listing, Offer
from .forms import OfferForm


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

def accept_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    # Only the listing owner can accept
    if request.user != offer.listing.owner:
        return redirect('listing_detail', pk=offer.listing.id)

    # Mark this offer as accepted
    offer.status = "accepted"
    offer.save()

    # Reject all other offers on the same listing
    Offer.objects.filter(listing=offer.listing).exclude(id=offer.id).update(status="rejected")

    # Mark the listing as pending
    offer.listing.status = "pending"
    offer.listing.save()

    return redirect('listing_detail', pk=offer.listing.id)


def reject_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    # Only the listing owner can reject
    if request.user != offer.listing.owner:
        return redirect('listing_detail', pk=offer.listing.id)

    offer.status = "rejected"
    offer.save()

    return redirect('listing_detail', pk=offer.listing.id)

def make_offer(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Prevent owners from offering on their own listing
    if request.user == listing.owner:
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.listing = listing
            offer.offered_by = request.user
            offer.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = OfferForm()

    return render(request, 'exchange/make_offer.html', {
        'listing': listing,
        'form': form,
    })

def confirm_exchange(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Only the two parties can confirm
    accepted_offer = listing.accepted_offer
    if not accepted_offer:
        return redirect('listing_detail', pk=pk)

    if request.user not in [listing.owner, accepted_offer.offered_by]:
        return redirect('listing_detail', pk=pk)

    # Mark listing as completed
    listing.status = "completed"
    listing.save()

    return redirect('listing_detail', pk=pk)







    
