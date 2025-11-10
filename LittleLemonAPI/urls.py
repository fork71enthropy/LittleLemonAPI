from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
#write all your paths here

urlpatterns = [
    #first functionnality (authentication)
    path('auth/',include('djoser.urls')),  
    path('auth/',include('djoser.urls.authtoken')),  

    #second functionnality (menu-items endpoints)
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('api-token-auth',obtain_auth_token),
]





