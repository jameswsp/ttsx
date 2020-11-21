from django.shortcuts import render, redirect

# Create your views here.

def add_cart(request):
    """ 添加购物车到cookie，goods_id:count"""
    # 获取传入的id
    goods_id = request.GET.get("id","")
    print(request.GET)
    # 将商品ID存入cookie
    if goods_id:
        print("goods_id = " + goods_id)
        prev_url = request.META.get("HTTP_REFERER",'')
        print("--- " + prev_url)
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id)
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1
        response.set_cookie(goods_id, goods_count)
    else:
        print("goods_id = " + goods_id)

    return response