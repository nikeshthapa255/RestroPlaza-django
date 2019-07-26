from django.urls import path, include
from .views import (
    UserCreate,
    RestaurantView,
    LoginView,
    getOwnerRestro,
    DishView,
    DishDetailView
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter





app_name = "resturant"


# router = DefaultRouter()
# router.register(r'"restaurant/<int:Rpk>/dish', DishView)
# router.register(r'restro',RestaurantViewSet)

urlpatterns = [
    path('user/', UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("restaurant/", RestaurantView.as_view(), name="restaurant"),
    path("restaurantByToken/", getOwnerRestro.as_view(), name="getOwnerRestro"),
    path("restaurant/<int:Rpk>/dish/",DishView.as_view()),
    path("restaurant/<int:Rpk>/dish/<int:pk>/",DishDetailView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
