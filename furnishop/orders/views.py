import uuid
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart
from orders.tasks import send_order_confirmation_email


# ავტორიზებული მომხმარებლის ყველა შეკვეთა
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


# კონკრეტული შეკვეთის დეტალები (id-ის მიხედვით)
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# ახალი შეკვეთის შექმნა (კალათიდან)
class CreateOrderView(generics.GenericAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shipping_address = serializer.validated_data['shipping_address']
        phone = serializer.validated_data['phone']
        notes = serializer.validated_data.get('notes', '')

        # მომხმარებლის კალათა
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total = cart.get_total_price()

        # შეკვეთის შექმნა
        order = Order.objects.create(
            user=request.user,
            order_number=str(uuid.uuid4().hex[:10]).upper(),
            total_amount=total,
            shipping_address=shipping_address,
            phone=phone,
            notes=notes,
        )

        # კალათიდან პროდუქტების OrderItem-ებად გადატანა
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,  # ფასი შეკვეთის მომენტში
            )

        # კალათის გასუფთავება შეკვეთის შექმნის შემდეგ
        cart.items.all().delete()

        # Asynchronous email send via Celery
        send_order_confirmation_email.delay(order.id)

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
