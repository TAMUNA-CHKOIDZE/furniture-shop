from django.urls import path
from orders.views import OrderListView, OrderDetailView, CreateOrderView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
]
