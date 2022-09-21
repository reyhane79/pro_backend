from rest_framework import serializers

from shop.models import  OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order_product', 'item']

    def save(self, **kwargs):
        order_item = OrderItem(order_product=self.validated_data['order_product'],
                               item=self.validated_data['item'])
        order_item.save()
        return order_item
