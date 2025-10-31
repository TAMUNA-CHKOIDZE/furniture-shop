from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # List view (Admin-ის მთავარი გვერდი)
    list_display = ('email', 'full_name', 'phone', 'address', 'is_active', 'is_staff')
    search_fields = ('first_name', 'last_name', 'phone')  # ძიება სახელით, გვარით და ტელეფონით
    list_filter = ('address',)  # ფილტრი მისამართით
    ordering = ('first_name', 'last_name')  # სორტირება სახელით და გვარით

    # View/Edit ფორმა
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Add User ფორმა
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'address', 'birth_date',
                       'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    # Full Name სვეტის გამოსახვა
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

