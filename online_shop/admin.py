from django.contrib.auth.models import User, Group

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
    list_display = ('id', 'title')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category_id', 'price', 'discount', 'is_very_expensive_product')
    search_fields = ['id', 'name', 'price']
    prepopulated_fields = {'slug': ('name',)}

    def is_very_expensive_product(self, obj):
        return obj.price > 500

    is_very_expensive_product.boolean = True


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_id', 'email', 'body')
    search_fields = ['name', 'email', 'body']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'quantity', 'phone')
    search_fields = ['name', 'phone', 'product']
