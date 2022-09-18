
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product
from product.serializer import AddProductSerializer, GetProductSerializer
from users.models import Shop, CustomUser


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    shop = Shop.objects.get(user=request.user)
    serializer = AddProductSerializer(data=request.data,
                                      context={'shop': shop})
    if serializer.is_valid():
        product = serializer.save()
        if 'description' in request.POST:
            product.description = request.POST.get('description')
            product.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_customer:
        products = Product.objects.all()
        serializer = GetProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        shop = Shop.objects.get(user=user)
        products = Product.objects.filter(shop=shop)
        serializer = GetProductSerializer(products, many=True)
        return Response(serializer.data)

