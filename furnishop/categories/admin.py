from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'slug', 'created_at')
    search_fields = ('name',)  # ძიება სახელით
    list_filter = ('is_active',)  # ფილტრი is_active-ის მიხედვით
    prepopulated_fields = {'slug': ('name',)}  # slug-ის ავტომატური გენერაცია
