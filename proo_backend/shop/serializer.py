from rest_framework import serializers

from product.serializer import GetProductSerializer, GetItemSerializer
from shop.models import OrderItem, Order, OrderProduct


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order_product', 'item']

    def save(self, **kwargs):
        order_item = OrderItem(order_product=self.validated_data['order_product'],
                               item=self.validated_data['item'])
        order_item.save()
        return order_item


class GetOrderItemSerializer(serializers.ModelSerializer):
    item = GetItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'item']


class GetOrderProductSerializer(serializers.ModelSerializer):
    product = GetProductSerializer()
    items = serializers.SerializerMethodField('get_order_items')

    @staticmethod
    def get_order_items(order_product):
        items = OrderItem.objects.filter(order_product=order_product)
        serializer = GetOrderItemSerializer(items, many=True)
        return serializer.data

    class Meta:
        model = OrderProduct
        fields = ['product', 'id', 'items']


class GetOrderSerializer(serializers.ModelSerializer):
    order_products = serializers.SerializerMethodField('get_order_products')

    @staticmethod
    def get_order_products(order):
        order_products = OrderProduct.objects.filter(order=order)
        serializer = GetOrderProductSerializer(order_products, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ['price', 'id', 'max_delivery_time', 'minimum_delivery_time', 'state', 'tracking_code',
                  'order_products']
