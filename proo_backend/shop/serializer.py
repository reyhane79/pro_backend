from rest_framework import serializers

from shop.models import Order


class AddOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = []