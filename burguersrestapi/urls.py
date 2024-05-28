from django.urls import path, include
from burguersrestapi.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'burguers', BurgerViewSet)
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'drinks', DrinkViewSet, basename='drink')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUserView.as_view()),
    path('auth-status/', auth_status, name='auth-status'),
]