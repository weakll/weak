from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, ReviewViewSet, register_view, login_view, logout_view, me_view, join_view, merchant_profile_view, merchant_products_view, merchant_product_detail_view, event_list_view, today_special_view

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register_view, name='api-register'),
    path('auth/login/', login_view, name='api-login'),
    path('auth/logout/', logout_view, name='api-logout'),
    path('auth/me/', me_view, name='api-me'),
    path('join/', join_view, name='api-join'),
    path('events/', event_list_view, name='api-events'),
    path('todays-special/', today_special_view, name='api-todays-special'),
    path('merchant/profile/', merchant_profile_view, name='api-merchant-profile'),
    path('merchant/products/', merchant_products_view, name='api-merchant-products'),
    path('merchant/products/<int:product_id>/', merchant_product_detail_view, name='api-merchant-product-detail'),
]
