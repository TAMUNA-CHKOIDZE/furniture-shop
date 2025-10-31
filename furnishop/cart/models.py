from django.db import models
from django.conf import settings

from products.models import Product


# ---------- CART ----------
class Cart(models.Model):
    # თითო მომხმარებელს (User) ექნება მხოლოდ ერთი კალათა (Cart)
    # და თითო კალათა ეკუთვნის მხოლოდ ერთ კონკრეტულ მომხმარებელს.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="User"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Date')

    # ჯამური ფასი
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    #  კალათაში არსებული პროდუქტების სია
    def get_total_items(self):
        return [item.product for item in self.items.all()]

    # კალათაში არსებული პროდუქტების რაოდენობა
    def get_total_items_count(self):
        return sum(item.quantity for item in self.items.all())

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"Cart for {self.user.email}"


# ---------- CARTITEM ----------
# CartItem მოდელი წარმოადგენს კალათის ერთ კონკრეტულ პროდუქტს
class CartItem(models.Model):
    # ForeignKey ნიშნავს: თითო CartItem ეკუთვნის ერთ კალათას, მაგრამ თითო Cart-ში შეიძლება იყოს ბევრი CartItem.
    # ანუ ურთიერთობაა "ერთი Cart ბევრი CartItem".
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,  # კალათის წაშლისას ავტომატურად წაიშლება მისი ყველა CartItem
        related_name='items',  # კალათში არსებული items-ებთან წვდომისთვის
        verbose_name="Cart"
    )
    # product უკავშირდება Product მოდელს. თითო CartItem დაკავშირებულია ერთ კონკრეტულ პროდუქტთან
    # ერთი Product შეიძლება იყოს მრავალი CartItem-ის ნაწილი სხვადასხვა მომხმარებლის კალათაში.
    # ანუ ურთიერთობაა: ერთი Product ბევრ CartItem-ში შეიძლება იყოს გამოყენებული
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # თუ წავშლით პროდუქტს, მისი ყველა CartItem-იც წაიშლება
        related_name='cart_items',
        # საშუალებას გვაძლევს პროდუქტიდან წვდომა გქონდეს იმ CartItem-ებზე, სადაც ეს პროდუქტი დევს
        verbose_name="Product"
    )
    # თითო CartItem-ს აქვს რაოდენობა (რამდენი ერთეული პროდუქტი დევს კალათაში), რომელიც უნდა იყოს დადებითი რიცხვი
    # default=1 ნიშნავს, რომ როცა ვქმნით ახალ CartItem-ს, ავტომატურად რაოდენობა იქნება 1
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    # კალათის ჯამური ფასის დასათვლელად
    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
