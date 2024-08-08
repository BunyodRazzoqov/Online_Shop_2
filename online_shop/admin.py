from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.contrib import admin

from online_shop.models import Product, Category, Comment, Order

# Register your models here.

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Comment)
# admin.site.register(Order)

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product_count')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category_id', 'price', 'discount', 'is_very_expensive_product', 'preview')
    search_fields = ['id', 'name', 'price']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category']
    # fields = ('price', 'discounted_price',)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')

    preview.short_description = 'Image'

    def is_very_expensive_product(self, obj):
        return obj.price > 500

    is_very_expensive_product.boolean = True
    is_very_expensive_product.short_description = 'Is this product very expensive?'


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id', 'email', 'body', 'is_provide')
    search_fields = ['name', 'email', 'body']
    list_filter = ['name', 'email']

    def is_provide(self, obj):
        return obj.is_provide()

    is_provide.boolean = True
    is_provide.short_description = ' Is Provide'


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'quantity', 'phone')
    search_fields = ['name', 'phone', 'product']
    list_filter = ['name', 'phone']
