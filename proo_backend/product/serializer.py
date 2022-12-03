from rest_framework import serializers

from product.models import Product, ItemCategory, Item, ProductCategory


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'price', 'stock', 'category']

    def save(self, **kwargs):
        product = Product(shop=self.context.get('shop'),
                          title=self.validated_data['title'],
                          price=self.validated_data['price'],
                          stock=self.validated_data['stock'],
                          category=self.validated_data['category'])
        product.save()
        return product


class GetProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'icon']


class GetProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'price', 'stock', 'description', 'id', 'shop', 'category']


class AddItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCategory
        fields = ['product', 'title']

    def save(self, **kwargs):
        item_category = ItemCategory(product=self.validated_data['product'],
                                     title=self.validated_data['title'])
        item_category.save()
        return item_category


class AddItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['category', 'title']

    def save(self, **kwargs):
        item = Item(title=self.validated_data['title'],
                    category=self.validated_data['category'])
        item.save()
        return item


class GetItemCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCategory
        fields = ['id', 'title']


class GetItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'title', 'description']
