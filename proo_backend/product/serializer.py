from rest_framework import serializers

from product.models import Product


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'price', 'stock', 'category']

    def save(self, **kwargs):
        product = Product(shop=self.context.get('shop'),
                          title=self.validated_data['title'],
                          price=self.validated_data['price'],
                          stock=self.validated_data['stock'],
                          category_id=self.validated_data['category'])
        product.save()
        return product


class GetProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'price', 'stock', 'description', 'id', 'shop', 'category']
