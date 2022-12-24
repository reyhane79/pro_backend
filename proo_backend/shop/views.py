from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product, Item
from shop.models import Order, OrderProduct, Wallet, Comment
from shop.serializer import OrderItemSerializer, GetOrderSerializer, AddCommentSerializer, AddReplySerializer, \
    GetCommentSerializer

# for adding a product to shopping list
from users.models import CustomUser, Shop


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_product(request):
    try:
        order = Order.objects.get(user=request.user, state=False)
        product = Product.objects.get(id=request.POST.get('product'))

        if OrderProduct.objects.filter(order=order).first().product.shop == product.shop:
            if product.stock > 0:
                order_product = OrderProduct(order=order,
                                             product_id=request.POST.get('product'),
                                             count=request.POST.get('count'))
                order_product.save()
                order.price += product.price * float(order_product.count)
                order.save()
                return Response({'order_product': order_product.id})
            else:
                return Response({'error': 'out of stock'})

        else:
            return Response({'error': 'not same shop'})

    except Order.DoesNotExist:
        order = Order(user=request.user)
        order.save()
        product = Product.objects.get(id=request.POST.get('product'))

        if product.stock > 0:
            order_product = OrderProduct(order=order,
                                         product_id=request.POST.get('product'),
                                         count=request.POST.get('count'))
            order_product.save()
            order.price += product.price * float(order_product.count)
            order.save()
            return Response({'order_product': order_product.id})
        else:
            return Response({'error': 'out of stock'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_order_product(request):
    order_product = OrderProduct.objects.get(id=request.POST.get('order_product'))
    order_product.delete()
    return Response(status=status.HTTP_200_OK)


# for customizing product items
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_item(request):
    item = Item.objects.get(id=request.POST.get('item'))

    if item.is_available:
        serializer = OrderItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else:
        return Response({'error': 'item not available'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_order_item(request):
    item = Item.objects.get(id=request.POST.get('order_item'))
    item.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    try:
        order = Order.objects.get(user=request.user, state=False)
        serializer = GetOrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finish_order(request):
    order = Order.objects.get(user=request.user, state=False)
    order.price += OrderProduct.objects.filter(order=order).first().product.shop.delivery_cost
    order.save()
    wallet = Wallet.objects.get(user=request.user)
    if wallet.credit >= order.price:
        order.state = True
        order.stage = 2
        order.tracking_code = order.id
        order.save()
        wallet.credit -= order.price
        wallet.save()
        return Response({'message': 'خرید با موفقیت انجام شد'})
    else:
        return Response({'error': 'موجودی کیف پول کافی نیست'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = CustomUser.objects.get(id=request.user.id)

    if user.is_customer:
        orders = Order.objects.filter(user=user)

    else:
        shop = Shop.objects.get(user=user)
        orders = Order.objects.filter(orderproduct__product__shop=shop,
                                      state=True).distinct()
        if 'stage' in request.POST:
            orders = orders.filter(stage=request.POST.get('stage'))

    serializer = GetOrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_order_stage_by_shop(request):
    order = Order.objects.get(id=request.POST.get('order'))
    if request.POST.get('stage') == '3':
        if 'minimum_delivery_time' and 'max_delivery_time' in request.POST:
            order.minimum_delivery_time = request.POST.get('minimum_delivery_time')
            order.max_delivery_time = request.POST.get('max_delivery_time')
            order.stage = 3
            order.save()
            return Response({'message': 'سفارش درحال آماده سازی است'})
        else:
            return Response({'message': 'زمان ارسال را وارد کنید'})
    elif request.POST.get('stage') == '4':
        order.stage = 4
        order.save()
        return Response({'message': 'سفارش درحال ارسال است'})
    return Response({'message': 'bad request'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_order_stage_by_customer(request):
    order = Order.objects.get(id=request.POST.get('order'))
    if request.POST.get('stage') == '5':
        order.stage = 5
    elif request.POST.get('stage') == '6':
        order.stage = 6
    order.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request):
    serializer = AddCommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reply(request):
    serializer = AddReplySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_comments(request):
    user = CustomUser.objects.get(id=request.user.id)

    if user.is_customer:
        comments = Comment.objects.filter(order__orderproduct__product__shop_id=request.POST.get('shop')).distinct()
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data)
    else:
        shop = Shop.objects.get(user=user)
        comments = Comment.objects.filter(order__orderproduct__product__shop_id=shop.id).distinct()
        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data)
