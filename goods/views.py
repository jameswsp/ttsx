from django.http import HttpResponse
from django.shortcuts import render

from goods.models import *


# Create your views here.

def index(request):
    # 查询商品的分类
    categories = GoodsCategory.objects.all()

    # 从每个分类中获取4个商品，每一类商品的最后四个商品
    for cag in categories:
        # GoodsInfo.objects.filter(goods_cag=cag)
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]  # <GoodsInfo>_set, order by 是排序，根据ID排序，反向4个

    # 获取购物车里所有的商品，购物车的商品总数量, cookie

    cart_goods_list = []  # 读取购物车商品列表
    cart_goods_count = 0  # 商品的数量
    for goods_id, goods_num in request.COOKIES.items():  # cookie 存储的都是字符串
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    # 汇总数据

    return render(request, 'index.html', {'categories': categories
        , 'cart_goods_list': cart_goods_list
        , 'cart_goods_count': cart_goods_count
                                          }
                  )


def detail(request):
    # 1. 商品的分类
    categories = GoodsCategory.objects.all()
    # 2. 购物车数据
    ## 所有的购物车商品
    ## 购物车商品的总数量
    cart_goods_list = []
    cart_goods_count = 0
    # 获取购物车信息, goods_id:count
    for goods_id, goods_num in request.COOKIES.items():
        # 验证是否为商品
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.num = goods_num
        cart_goods_list.append(cart_goods)
        # 累加所有的商品数量得到总数量
        cart_goods_count = cart_goods_count + int(goods_num)

    # 获取querystring的商品ID
    goods_id = request.GET.get('id', 1)
    goods_data = GoodsInfo.objects.get(id=goods_id)

    # 3. 当前要显示的商品的数据
    return render(request, 'detail.html', {"categories": categories,
                                           "cart_goods_list": cart_goods_list,
                                           "cart_goods_count": cart_goods_count,
                                           "goods_data": goods_data
                                           })
