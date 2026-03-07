from django import forms
from .models import Item, Listing

class CreateListingForm(forms.Form):
    LISTING_TYPE_CHOICES = [
        ("item_for_silver", "Offer an item for silver"),
        ("silver_for_item", "Offer silver for an item"),
    ]

    listing_type = forms.ChoiceField(choices=LISTING_TYPE_CHOICES)

    # Fields for item-for-silver
    item_name = forms.CharField(required=False)
    item_description = forms.CharField(widget=forms.Textarea, required=False)
    desired_silver_oz = forms.DecimalField(required=False)

    # This field is no longer used but kept for compatibility
    item_estimated_value_oz = forms.DecimalField(required=False)

    # Fields for silver-for-item
    bullion_amount_oz = forms.DecimalField(required=False)
    desired_item_description = forms.CharField(required=False)

    def clean(self):
        cleaned = super().clean()
        listing_type = cleaned.get("listing_type")

        if listing_type == "item_for_silver":
            required_fields = ["item_name", "item_description", "desired_silver_oz"]
            for field in required_fields:
                if not cleaned.get(field):
                    self.add_error(field, "This field is required for item-for-silver listings.")

        elif listing_type == "silver_for_item":
            required_fields = ["bullion_amount_oz", "desired_item_description"]
            for field in required_fields:
                if not cleaned.get(field):
                    self.add_error(field, "This field is required for silver-for-item listings.")

        return cleaned

