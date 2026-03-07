from django.urls import path
from .views import dashboard_view
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("marketplace/", views.marketplace_index, name="marketplace_index"),
    path("listing/create/", views.create_listing, name="create_listing"),
    path("signup/", views.signup, name="signup"),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),

]


