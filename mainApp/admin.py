from django.contrib import admin

from .models import *
admin.site.register((Buyer, 
                     Brand,
                     Product,
                     Checkout,
                     CheckoutProducts,
                     Wishlist,))


@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
