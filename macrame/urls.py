
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views as mainApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainApp.home),
    path('shop/<str:mc>/<str:sc>/', mainApp.shoppage),
    path('single-product/', mainApp.singleproduct),
    path('price-filter/<str:mc>/<str:sc>/', mainApp.pricefilter),
    path('sort-filter/<str:mc>/<str:sc>/', mainApp.sortfilter),
    path('search/', mainApp.searchpage),
    path('single-product/<int:num>/', mainApp.singleproduct),
    path('login/', mainApp.loginpage),
    path('service/', mainApp.servicepage),
    path('about/', mainApp.aboutpage),
    path('checkout/', mainApp.checkoutpage),
    path('signup/', mainApp.signuppage),
    path('logout/', mainApp.logoutpage),
    path('contact/', mainApp.contactpage),
    path('profile/', mainApp.profilepage),
    path('update-profile/', mainApp.updateprofilepage),
    path('add-to-cart/<int:num>/', mainApp.AddToCart),
    path('cart/', mainApp.cartPage),
    path('delete/<str:id>/', mainApp.deletepage),
    path('update-cart/<str:id>/<str:op>/', mainApp.UpdateCartPage),
    path('place-order/', mainApp.placeOrder),
    path('confirmation/', mainApp.confirmationpage),
    path('add-to-wishlist/<int:num>/', mainApp.addToWishlist),
    path('forget-1/',mainApp.forgetPasswordPage1),
    path('forget-2/',mainApp.forgetPasswordPage2),
    path('forget-3/',mainApp.forgetPasswordPage3),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
