
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product, ItemCategory, Item, ProductCategory
from product.serializer import AddProductSerializer, GetProductSerializer, AddItemCategorySerializer, AddItemSerializer, \
    GetItemCategorySerializer, GetItemSerializer, GetProductCategorySerializer
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
def get_product_categories(request):
    categories = ProductCategory.objects.all()
    serializer = GetProductCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_product(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_customer:
        if 'category' in request.POST:
            products = Product.objects.filter(shop_id=request.POST.get('shop'),
                                              category_id=request.POST.get('category'))
            serializer = GetProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = Product.objects.filter(shop_id=request.POST.get('shop'))
            serializer = GetProductSerializer(products, many=True)
            return Response(serializer.data)
    else:
        shop = Shop.objects.get(user=user)
        products = Product.objects.filter(shop=shop)
        serializer = GetProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_category(request):
    serializer = AddItemCategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    serializer = AddItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_item_category(request):
    categories = ItemCategory.objects.filter(product=request.POST.get('product'))
    serializer = GetItemCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_items(request):
    categories = Item.objects.filter(category=request.POST.get('category'))
    serializer = GetItemSerializer(categories, many=True)
    return Response(serializer.data)
