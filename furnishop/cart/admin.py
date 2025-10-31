from django.contrib import admin

from cart.models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# ფილტრი მომხმარებლის მიხედვით, ასევე tabular inline-ის გამოყენებით
# მოდელის დეტალურზე დაამატებულია მისი მოკავშერე მოდელი CartItem
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at', 'get_total_price', 'get_total_items_count')
    list_filter = ('user',)
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = "Total Price"

    def get_total_items_count(self, obj):
        return obj.get_total_items_count()

    get_total_items_count.short_description = "Items Count"
