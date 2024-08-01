from itertools import product
from typing import Optional
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.shortcuts import render

from online_shop.forms import CommentModelForm, OrderModelForm
from online_shop.models import Product, Category, Comment


# Create your views here.


def product_list(request, category_id: Optional[int] = None):
    categories = Category.objects.all().order_by('id')
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'online_shop/home.html', context)


def product_detail(request, product_id):
    comments = Comment.objects.filter(product=product_id, is_provide=True).order_by('-id')
    product = Product.objects.get(id=product_id)
    context = {'product': product, 'comments': comments}
    return render(request, 'online_shop/detail.html', context)


# def add_comment(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         body = request.POST.get('body')
#         comment = Comment(name=name, email=email, body=body)
#         comment.product = product
#         comment.save()
#         return redirect('product_detail', product_id)
#
#     else:
#         pass
#     return render(request, 'online_shop/detail.html')


def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id)
    else:
        form = CommentModelForm()
    context = {'form': form, 'product': product}

    return render(request, 'online_shop/detail.html', context)


def add_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            product.quantity -= int(form.data.get('quantity'))
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('product_detail', product_id)
    else:
        form = OrderModelForm()
    context = {'form': form, 'product': product}
    return render(request, 'online_shop/detail.html', context)
