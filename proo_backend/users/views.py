
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from shop.models import Wallet
from users.models import CustomUser, Shop
from users.serializers import CustomUserSerializer, ShopSerializer, CostumerSerializer, GetShopSerializer, \
    GetUserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        if 'is_shop' in request.POST:
            shop_serializer = ShopSerializer(data=request.data,
                                             context={'user': user})
            if shop_serializer.is_valid():
                user.is_sailor = True
                user.save()
                shop_serializer.save()
                return Response(shop_serializer.data)
            else:
                user.delete()
                return Response(shop_serializer.errors)
        elif 'is_customer' in request.POST:
            customer_serializer = CostumerSerializer(data=request.data,
                                                     context={'user': user})
            if customer_serializer.is_valid():
                user.is_customer = True
                user.save()
                customer_serializer.save()
                wallet = Wallet(user=user, credit=1000000)
                wallet.save()
                return Response(customer_serializer.data)
            else:
                user.delete()
                return Response(customer_serializer.errors)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    response = dict()
    try:
        user = CustomUser.objects.get(phone=request.POST.get('phone'))
        if user.check_password(request.POST.get('password')):
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            response['token'] = token.key
            if user.is_customer:
                response['user_type'] = 'customer'
            else:
                response['user_type'] = 'shop'
        else:
            response['message'] = 'password is incorrect'

        return Response(response)
    except CustomUser.DoesNotExist:
        response['message'] = 'user with this phone not exist'
        return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    Token.objects.filter(user=user).delete()
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if user.check_password(request.POST.get('password')):
        user.set_password(request.POST.get('new_password'))
        user.save()
        return Response({'message': 'password changed'})
    else:
        return Response({'message': 'password is incorrect'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_shop_list(request):
    shop = Shop.objects.all()
    if 'search' in request.POST:
        shop = shop.filter(user__name__contains=request.POST.get('search'))
    serializer = GetShopSerializer(shop, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_info(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_customer:
        serializer = GetUserSerializer(user)
        return Response(serializer.data)
    elif user.is_sailor:
        shop = Shop.objects.get(user=user)
        serializer = GetShopSerializer(shop)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token(request):
    return Response(status=status.HTTP_200_OK)
