from rest_framework import serializers
from burguersrestapi.models import *

from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


#
# Model serializers
#
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        orderDayHour = data.get('orderDayHour')
        findOrdersPerDayHour = Order.objects.filter(orderDayHour=orderDayHour)
        if(findOrdersPerDayHour.count() >= 4):
            raise ValidationError('There are 4 orders programmed for this hour today.')
        return data
    
    
    
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'

# To only pass certain fields to the Front-End
class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','price', 'image']

class BurgerSerializer(serializers.ModelSerializer):
    refProduct = ProductSerializer()
    class Meta:
        model = Burger
        fields = '__all__'
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        product_data = validated_data.pop('refProduct')
        product = Product.objects.create(**product_data)
        burger = Burger.objects.create(refProduct = product, **validated_data)
        burger.ingredients.set(ingredients_data)
        return burger

class DrinkSerializer(serializers.ModelSerializer):
    refProduct = ProductSerializer()

    class Meta:
        model = Drink
        fields = '__all__'
    def create(self, validated_data):
        product_data = validated_data.pop('refProduct')
        product = Product.objects.create(**product_data)
        drink = Drink.objects.create(refProduct = product, **validated_data)
        return drink

#
# User auth serializers
#
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]    
    )
    password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    # Check if the passwords match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user: 
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both username and password are required")
        attrs['user'] = user
        return attrs
