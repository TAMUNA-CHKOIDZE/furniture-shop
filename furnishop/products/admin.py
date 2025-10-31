from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'color', 'material', 'is_available', 'featured')
    list_editable = ('price', 'stock')  # ფასის და მარაგის რედაქტირება პირდაპირ სიაში
    search_fields = ('name',)  # ძიება სახელით
    list_filter = ('category', 'color', 'material')  # ფილტრი კატეგორიის, ფერის, მასალის მიხედვით
    prepopulated_fields = {'slug': ('name',)}  # slug-ის ავტომატური გენერაცია
