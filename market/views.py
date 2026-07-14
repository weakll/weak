from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Store, Review, MerchantProfile, Event, TodaySpecial, Product
from .serializers import (
    StoreListSerializer, StoreDetailSerializer,
    ReviewSerializer, UserRegisterSerializer, UserLoginSerializer, UserInfoSerializer, MerchantStoreSerializer, MerchantProductSerializer,
    JoinApplicationSerializer,
    EventSerializer,
    TodaySpecialSerializer
)

class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        return StoreDetailSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        store_id = self.request.query_params.get('store_id')
        if store_id:
            qs = qs.filter(store_id=store_id)
        return qs

    @action(detail=False, methods=['post'])
    def submit(self, request):
        data = request.data.copy()
        if request.user.is_authenticated:
            data['nickname'] = request.user.username
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email or '',
            'avatar': '',
        }, status=status.HTTP_201_CREATED)
    errors = serializer.errors
    if 'username' in errors:
        return Response({'error': '该用户名已被注册'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': '注册失败，请检查输入'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email or '',
                'avatar': '',
            })
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': '请填写用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email or '',
        'avatar': '',
    })
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def join_view(request):
    serializer = JoinApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': '提交成功，我们会尽快联系您'}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'message': '请填写姓名和联系电话'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def merchant_profile_view(request):
    try:
        profile = MerchantProfile.objects.get(user=request.user, is_approved=True)
    except MerchantProfile.DoesNotExist:
        return Response({"error": "商家账号未激活或未分配店铺"}, status=403)
    store = profile.store
    if not store:
        return Response({"error": "未分配店铺"}, status=404)
    if request.method == "GET":
        serializer = MerchantStoreSerializer(store)
        return Response(serializer.data)
    serializer = MerchantStoreSerializer(store, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def merchant_products_view(request):
    try:
        profile = MerchantProfile.objects.get(user=request.user, is_approved=True)
    except MerchantProfile.DoesNotExist:
        return Response({"error": "商家账号未激活"}, status=403)
    if not profile.store:
        return Response({"error": "未分配店铺"}, status=404)
    if request.method == "GET":
        products = profile.store.products.all()
        serializer = MerchantProductSerializer(products, many=True)
        return Response(serializer.data)
    serializer = MerchantProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(store=profile.store)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def merchant_product_detail_view(request, product_id):
    try:
        profile = MerchantProfile.objects.get(user=request.user, is_approved=True)
    except MerchantProfile.DoesNotExist:
        return Response({"error": "商家账号未激活"}, status=403)
    try:
        product = profile.store.products.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "商品不存在"}, status=404)
    if request.method == "PUT":
        serializer = MerchantProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    product.delete()
    return Response(status=204)


@api_view(["GET"])
@permission_classes([AllowAny])
def event_list_view(request):
    past = request.query_params.get("past", "false").lower() == "true"
    if past:
        events = Event.objects.filter(status="archived")
    else:
        events = Event.objects.filter(status="published")
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def today_special_view(request):
    special = TodaySpecial.objects.filter(is_active=True).first()
    if special:
        serializer = TodaySpecialSerializer(special)
        return Response(serializer.data)
    return Response(None)
