from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *
from .permissions import IsOwner

# Create your views here.
# Model viewsets
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type = self.request.query_params.get('productType',None)
        if product_type is not None:
            queryset = queryset.filter(productType=product_type)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer

class BurgerViewSet(viewsets.ModelViewSet):
    queryset = Burger.objects.all()
    serializer_class = BurgerSerializer


# User-related viewsets
class RegisterUserView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class LoginUserView(generics.GenericAPIView):
  permission_classes = (AllowAny,)
  serializer_class = LoginSerializer

  def post(self,request,*args,**kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

class LogoutUserView(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@login_required
def auth_status(request):
    return JsonResponse({'authenticated': True})

# api-root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'burguers': reverse('burguer-list', request=request, format=format),
        'ingredients':reverse('ingredient-list',request=request,format=format),
        'dirnks':reverse('drinks-list', request=request,format=format),
        'orders':reverse('orders-list', request=request,format=format)
    })

#