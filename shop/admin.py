from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, ProductImage, Product, Supplier


# Register your models here.
# 分類管理
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'attr', 'slug', 'parent', 'ordering')


admin.site.register(Category, CategoryAdmin)


# 商品圖片管理
class ProductImageInLine(admin.StackedInline):
    model = ProductImage
    fields = ['product_image', 'image', 'ordering']
    readonly_fields = ['product_image']
    extra = 0

    def product_image(self, obj):
        return mark_safe('<img src="{}" width="100px"/>'.format(obj.image.url))

    product_image.allow_tags = True


# 商品圖片管理
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_data', 'image', 'ordering')


admin.site.register(ProductImage, ProductImageAdmin)


# 供應商管理
class SupplierInLine(admin.TabularInline):
    model = Supplier
    readonly_fields = ('updated',)
    fields = ['supplier', 'no', 'url', 'available', 'updated']
    raw_id_fields = ['product']
    extra = 0


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'no', 'url', 'available', 'updated')
    fields = ['supplier', 'no', 'url', 'available']


admin.site.register(Supplier, SupplierAdmin)


# 商品管理
class ProductAdmin(admin.ModelAdmin):
    ordering = ['-id']
    readonly_fields = ('updated',)
    list_display = ('id',
                    'no',
                    'image_data',
                    'name',
                    'price',
                    'stock',
                    'available',
                    'updated')
    fieldsets = (
        (None, {
            'fields': (('no', 'product_image'),)
        }),
        (None, {
            'fields': ('name', 'image', 'category', 'description',
                       ('price', 'stock', 'views'), 'available'),
        }),
    )
    filter_horizontal = ('category',)
    readonly_fields = ('no', 'product_image',)

    def product_image(self, obj):
        return mark_safe('<img src="{}" width="125px"/>'.format(obj.image.url))

    product_image.allow_tags = True
    product_image.short_description = '主圖預覽'

    inlines = [ProductImageInLine, SupplierInLine]


admin.site.register(Product, ProductAdmin)
