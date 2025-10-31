from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from orders.choices import STATUS_CHOICES
from products.models import Product

# Georgian phone number validator
phone_validator = RegexValidator(
    regex=r'^\d{8,9}$',
    message="Enter only the phone number digits, e.g. 599123456"
)


# ---------- ORDER ----------
class Order(models.Model):
    # ეს ველი მიუთითებს რომელი მომხმარებელი ქმნის შეკვეთას. ForeignKey – დაკავშირება სხვა მოდელთან (CustomUser).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # თუ მომხმარებელი წაიშლება, ყველა მისი შეკვეთა ავტომატურად წაიშლება.
        related_name='orders',  # მომხმარებლის მიხედვით შეგვიძლია მივწვდეთ ყველა შეკვეთას
        verbose_name="User"
    )
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Order Number")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Status")
    # შეკვეთის ჯამური თანხა დოლარებში
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount ($)")
    # შეკვეთის მისამართი, სადაც უნდა გაიგზავნოს პროდუქტი
    shipping_address = models.TextField(verbose_name="Shipping Address")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name='Phone Number')
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Date')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        """Automatically add '+995' prefix if it's missing."""
        if self.phone and not self.phone.startswith('+995'):
            self.phone = f'+995{self.phone}'
        super().save(*args, **kwargs)


# ---------- ORDER ITEM ----------
# ერთი Order შეიძლება რამდენიმე OrderItem-ს ჰქონდეს (ერთ შეკვეთაში რამდენიმე პროდუქტი)
class OrderItem(models.Model):
    # ეს ველი უკავშირდება Order-ს, ForeignKey (many-to-one ურთიერთობა): ერთი შეკვეთა - მრავალი OrderItem.
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Order"
    )
    # ეს ველი უკავშირდება კონკრეტულ პროდუქტს, რომელიც შეკვეთაშია (ერთ შეკვეთაში შეიძლება იყოს ბევრი პროდუქტი)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Product"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity")  # თითოეული პროდუქტის რაოდენობა შეკვეთაში (მხოლოდ დადებითი მთელი რიცხვები)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Price')  # პროდუქტის ფასი შეკვეთის მომენტში

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
