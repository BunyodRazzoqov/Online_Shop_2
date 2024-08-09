from django.urls import path
from online_shop.views import views
from online_shop.views import auth

urlpatterns = [
    path('product-list/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='category_detail_id'),
    path('product-detail/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:product_slug>/add-comment/', views.add_comment, name='add_comment'),
    path('product/<slug:product_slug>/add-order/', views.add_order, name='add_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),

    #     Authentication
    path('login-page/', auth.login_page, name='login_page'),
    path('register-page/', auth.register_page, name='register_page'),
    path('logout-page/', auth.logout_page, name='logout_page'),
]
