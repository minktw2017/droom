from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


# Create your views here.

def product_list(request, category_slug=None):
    parent = None
    parent_category = None
    category = None
    children = None

    request.session["web_path"] = "home"
    web_path = request.session.get("web_path", default="none")

    categories = Category.objects.filter(attr="first").order_by('ordering')
    object_list = Product.objects.filter(available=True).order_by('-id')
    
    # 設定分頁
    paginator = Paginator(object_list, 40)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        if category.children:
            parent = category_slug

        if category.parent:
            parent = category.parent.slug
            parent_category = get_object_or_404(Category, slug=category.parent.slug)

        object_list = object_list.filter(category=category).order_by('-id')
        request.session["web_path"] = category_slug
        web_path = request.session.get("web_path", default="home")
        request.session["parent"] = parent
        parent = request.session.get("parent", default="none")
            # 設定分頁
        paginator = Paginator(object_list, 40)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'page': page,
                   'web_path': web_path,
                   'parent': parent,
                   'parent_category': parent_category,
                   'children': children})


def product_detail(request, id, no):
    parent_category = None
    category = None
    parent = None
    
    categories = Category.objects.filter(attr="first").order_by('ordering')

    product = get_object_or_404(Product,
                                id=id,
                                no=no,
                                available=True)
    web_path = request.session.get("web_path")

    if not web_path == "home":
        category = get_object_or_404(Category, slug=web_path)

    else:
        category_slug = product.category.all().filter(attr='first')[0].slug
        category = get_object_or_404(Category, slug=category_slug)

    if category.parent:
        parent = category.parent.slug
        parent_category = get_object_or_404(Category, slug=category.parent.slug)

    cart_product_form = CartAddProductForm()

    product.increase_views()
    images = ProductImage.objects.filter(product_id=id)
    return render(request,
                  'shop/product/detail.html',
                  {'category': category,
                   'categories': categories,
                   'product': product,
                   'web_path': web_path,
                   'parent': parent,
                   'parent_category': parent_category,
                   'cart_product_form': cart_product_form,
                   'images': images})
