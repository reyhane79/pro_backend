from rest_framework import serializers

from users.models import CustomUser, Shop, Customer


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['phone', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        user = CustomUser(phone=self.validated_data['phone'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['address', 'delivery_cost', 'start_time', 'end_time']

    def save(self, **kwargs):
        shop = Shop(address=self.validated_data['address'],
                    delivery_cost=self.validated_data['delivery_cost'],
                    start_time=self.validated_data['start_time'],
                    end_time=self.validated_data['end_time'],
                    user=self.context.get('user'))
        shop.save()
        return shop


class CostumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['gender']

    def save(self, **kwargs):
        customer = Customer(gender=self.validated_data['gender'],
                            user=self.context.get('user'))
        customer.save()
        return customer
