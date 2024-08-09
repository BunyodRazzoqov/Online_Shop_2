from itertools import product
from typing import Optional

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.shortcuts import render

from online_shop.forms import CommentModelForm, OrderModelForm, ProductModelForm
from online_shop.models import Product, Category, Comment


# Create your views here.


def product_list(request, category_slug: Optional[str] = None):
    categories = Category.objects.all().order_by('id')
    search = request.GET.get('q')
    filter_type = request.GET.get('filter', '')
    if category_slug:
        if filter_type == 'expensive':
            products = Product.objects.filter(category__slug=category_slug).order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.filter(category__slug=category_slug).order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(category__slug=category_slug) & Q(rating__gt=4)).order_by('-rating')
        else:
            products = Product.objects.filter(category__slug=category_slug)
    else:
        if filter_type == 'expensive':
            products = Product.objects.all().order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.all().order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(rating__gte=4)).order_by('-rating')
            print(products)

        else:
            products = Product.objects.all()

    if search:
        products = products.filter(Q(name__icontains=search) | Q(comments__name__icontains=search))

    context = {'products': products, 'categories': categories}
    return render(request, 'online_shop/home.html', context)


def product_detail(request, product_slug):
    search = request.GET.get('q')
    categories = Category.objects.all()
    comments = Comment.objects.filter(product__slug=product_slug, is_provide=True).order_by('-id')
    product = Product.objects.get(slug=product_slug)
    min_price = product.price * 0.7
    max_price = product.price * 1.3
    similar_products = Product.objects.filter(category=product.category, price__range=[min_price, max_price]).exclude(
        slug=product_slug)
    if search:
        comments = comments.filter(Q(name__icontains=search) | Q(body__icontains=search))
    context = {'product': product, 'comments': comments, 'categories': categories, 'similar_products': similar_products}
    return render(request, 'online_shop/detail.html', context)


def add_comment(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_slug)
    else:
        form = CommentModelForm()
    context = {'form': form, 'product': product}

    return render(request, 'online_shop/detail.html', context)


def add_order(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    form = OrderModelForm()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    message='You order submitted successfully!'
                )
                return redirect('product_detail', product_slug)
            else:
                messages.add_message(
                    request, level=messages.ERROR,
                    message='the number of products is limited'
                )
    context = {'form': form, 'product': product}
    return render(request, 'online_shop/detail.html', context)


# @login_required
def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {'form': form}

    return render(request, 'online_shop/add-product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id)
    return render(request, 'online_shop/edit-product.html', {'form': form})
