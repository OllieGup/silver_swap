from django.contrib import admin
from .models import Item, BullionHolding, Listing, Swap

admin.site.register(Item)
admin.site.register(BullionHolding)
admin.site.register(Listing)
admin.site.register(Swap)

