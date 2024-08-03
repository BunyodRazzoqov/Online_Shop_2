from django.contrib import admin
from django.urls import path
from online_shop import views

urlpatterns = [
    path('product-list/', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='category_detail_id'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add-comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/add-order/', views.add_order, name='add_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/',views.edit_product,name ='edit_product'),
]
