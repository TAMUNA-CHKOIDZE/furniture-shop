from django.urls import path, include

urlpatterns = [
    path('', include('products.urls')),
    path('', include('categories.urls')),
    path('', include('users.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
]
