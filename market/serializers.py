
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Store, Certificate, StaffMember, Product, Review, JoinApplication, MerchantProfile, Event, TodaySpecial

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TodaySpecialSerializer(serializers.ModelSerializer):
    store_image = serializers.URLField(source='store.image_url', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    class Meta:
        model = TodaySpecial
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'

class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_store_name(self, obj):
        return obj.store.name

class StoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'slug', 'category', 'image_url', 'rating', 'popularity',
                  'description', 'latitude', 'longitude', 'waiting', 'spicy', 'vegetarian']

class StoreDetailSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True, read_only=True)
    staff = StaffMemberSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    recent_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = '__all__'

    def get_recent_reviews(self, obj):
        reviews = obj.reviews.all()[:5]
        return ReviewSerializer(reviews, many=True).data

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']



class JoinApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinApplication
        fields = ['name', 'phone', 'application_type', 'message']




class MerchantStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'slug', 'category', 'description', 'address',
                  'image_url', 'opening_hours', 'phone', 'spicy', 'vegetarian']


class MerchantProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'special_price',
                  'image_url', 'is_recommended', 'spicy_level', 'is_vegetarian']

