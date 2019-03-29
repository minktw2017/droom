'''Main Product View'''
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from cart.forms import CartAddProductForm
from .models import (Category,
                     Product,
                     ProductImage,
                     GoodsProduct,
                     GoodsProductImage)


# Create your views here.
def product_list(request, category_slug=None):
    '''Initialize the render Dictionary'''
    parent = None
    parent_category = None
    category = None

    request.session["web_path"] = "home"
    web_path = request.session.get("web_path", default="none")

    categories = Category.objects.filter(attr="first", available=True).order_by('ordering')
    object_list = Product.objects.filter(available=True).order_by('-id')

    # 設定分頁
    paginator = Paginator(object_list, 36)
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
        paginator = Paginator(object_list, 36)
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
                   'parent_category': parent_category
                   })


def product_detail(request, p_id, p_no):
    '''Initialize the render Dictionary'''
    parent_category = None
    category = None
    parent = None

    categories = Category.objects.filter(attr="first").order_by('ordering')

    product = get_object_or_404(Product,
                                id=p_id,
                                no=p_no,
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

    #增加商品瀏覽次數
    product.increase_views()

    images = ProductImage.objects.filter(product_id=p_id)
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

def search(request):
    ''' Define Search Function'''
    template = 'shop/product/list.html'

    categories = Category.objects.filter(attr="first").order_by('ordering')

    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(no__icontains=query)
        )
    else:
        results = Product.objects.filter(available=True).order_by('-id')

    paginator = Paginator(results, 36)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'page': page,
        'query': query
    }

    return render(request, template, context)

def index(request):
    ''' GoodsProduct Index'''
    template = 'shop/product/index.html'
    object_list = Product.objects.filter(available=True)
    newest_category = Category.objects.filter(attr="newest", available=True)
    new_goods = object_list.filter(category=newest_category)

    hot_category = Category.objects.filter(attr="hot", available=True)
    hot_goods = object_list.filter(category=hot_category)

    re_category = Category.objects.filter(attr="recommend", available=True)
    re_goods = object_list.filter(category=re_category)

    fe_category = Category.objects.filter(slug="goods_female", available=True)
    fe_goods = object_list.filter(category=fe_category)

    ma_category = Category.objects.filter(slug="goods_male", available=True)
    ma_goods = object_list.filter(category=ma_category)

    ba_category = Category.objects.filter(slug="goods_bags", available=True)
    ba_goods = object_list.filter(category=ba_category)

    context = {
        'new_goods': new_goods,
        'hot_goods': hot_goods,
        're_goods': re_goods,
        'fe_goods': fe_goods,
        'ma_goods': ma_goods,
        'ba_goods': ba_goods
        }

    return render(request, template, context)


def goods_detail(request, p_id, p_no):
    ''' GoodsProduct detail'''
    template = 'shop/product/goods_detail.html'
    product = get_object_or_404(Product,
                                id=p_id,
                                no=p_no,
                                available=True)
    images = ProductImage.objects.filter(product_id=p_id)
    cart_product_form = CartAddProductForm()

    context = {'product': product,
               'images': images,
               'cart_product_form': cart_product_form}

    return render(request, template, context)
