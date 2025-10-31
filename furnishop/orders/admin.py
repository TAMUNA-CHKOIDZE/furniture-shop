from django.contrib import admin

from orders.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# ძიება შეკვეთის ნომრით და მომხმარებლის მიხედვით, ფილტრი სტატუსისა და თარიღის მიხედვით.
# ასევე tabular inline-ის გამოყენებით მოდელის დეტალურზე დაამატებულია მისი მოკავშერე მოდელი OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    search_fields = ('order_number', 'user__email')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
