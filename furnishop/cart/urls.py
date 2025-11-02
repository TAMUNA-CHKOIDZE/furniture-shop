from django.urls import path
from cart.views import CartDetailView, CartAddItemView, CartRemoveItemView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/remove/', CartRemoveItemView.as_view(), name='cart-remove'),
]
