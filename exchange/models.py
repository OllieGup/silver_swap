from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BullionHolding(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_oz = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight_oz} oz"


class Listing(models.Model):
    LISTING_TYPES = [
        ("item_for_silver", "Item for Silver"),
        ("silver_for_item", "Silver for Item"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("pending", "Pending Exchange"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # Item-for-silver fields
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)
    desired_silver_oz = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Silver-for-item fields
    bullion_amount_oz = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_item_description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listing #{self.id} ({self.listing_type})"

    @property
    def accepted_offer(self):
        return self.offers.filter(status="accepted").first()


class Swap(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Swap proposal for Listing #{self.listing.id}"

class Offer(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    offered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offers_made"
    )
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.offered_by} on Listing #{self.listing.id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


    
from django.contrib.auth.models import User

@property
def unread_notifications(self):
    return self.notifications.filter(is_read=False).count()

User.add_to_class("unread_notifications", unread_notifications)


