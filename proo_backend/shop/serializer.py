from rest_framework import serializers

from product.serializer import GetProductSerializer, GetItemSerializer
from shop.models import OrderItem, Order, OrderProduct, Comment, Reply


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
        fields = ['product', 'id', 'items', 'count']


class GetOrderSerializer(serializers.ModelSerializer):
    order_products = serializers.SerializerMethodField('get_order_products')
    stage = serializers.SerializerMethodField('get_stage')
    comment = serializers.SerializerMethodField('get_comment')

    def get_comment(self, order):
        try:
            comment = Comment.objects.get(order=order)
            serializer = GetCommentSerializer(comment)
            return serializer.data
        except Comment.DoesNotExist:
            return {
                'content': '',
                'reply': {
                    'content' : ''
                    }
            }

    def get_stage(self, order):
        if order.stage == '1':
            return 'تکمیل نشده'
        if order.stage == '2':
            return 'در انتظار تایید فروشگاه'
        if order.stage == '3':
            return 'در حال آماده سازی'
        if order.stage == '4':
            return 'در حال ارسال'
        if order.stage == '5':
            return 'دریافت شده'
        if order.stage == '6':
            return 'دریافت نشده'

    @staticmethod
    def get_order_products(order):
        order_products = OrderProduct.objects.filter(order=order)
        serializer = GetOrderProductSerializer(order_products, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ['price', 'id', 'max_delivery_time', 'minimum_delivery_time', 'state', 'tracking_code',
                  'order_products', 'stage', 'comment']


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['order', 'content', 'score']

    def save(self, **kwargs):
        comment = Comment(order=self.validated_data['order'],
                          content=self.validated_data['content'],
                          score=self.validated_data['score'])
        comment.save()
        return comment


class GetReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ['id', 'content']


class GetCommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField('get_reply')

    @staticmethod
    def get_reply(comment):
        try:
            reply = Reply.objects.get(comment=comment)
            return GetReplySerializer(reply).data
        except Reply.DoesNotExist:
            return {
                'content': ''
            }

    class Meta:
        model = Comment
        fields = ['id', 'score', 'content', 'reply']


class AddReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ['comment', 'content']

    def save(self, **kwargs):
        reply = Reply(content=self.validated_data['content'],
                      comment=self.validated_data['comment'])
        reply.save()
        return reply
