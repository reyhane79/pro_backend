
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product, Item
from shop.models import Order, OrderProduct
from shop.serializer import OrderItemSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_product(request):
    try:
        order = Order.objects.get(user=request.user, state=False)
        product = Product.objects.get(id=request.POST.get('product'))

        if OrderProduct.objects.filter(order=order).first().product.shop == product.shop:
            if product.stock > 0:
                order_product = OrderProduct(order=order,
                                             product_id=request.POST.get('product'))
                order_product.save()
                order.price = order.price+product.price
                order.save()
                return Response({'order_product': order_product.id})
            else:
                return Response({'error': 'out of stock'})

        else:
            return Response({'error': 'not same shop'})

    except Order.DoesNotExist:
        order = Order(user=request.user)
        order.save()
        order_product = OrderProduct(order=order,
                                     product_id=request.POST.get('product'))
        order_product.save()
        return Response({'order_product': order_product.id})


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

