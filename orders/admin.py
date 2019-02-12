from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'gender', 'email', 'postal_code',
                    'address', 'phone', 'created', 'updated', 'paid', 'status']
    list_filter = ['paid', 'status', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
