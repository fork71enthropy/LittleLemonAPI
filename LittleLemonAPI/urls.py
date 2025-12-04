from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
#write all your paths here

urlpatterns = [
    #first functionnality (authentication)
    path('auth/',include('djoser.urls')),  
    path('auth/',include('djoser.urls.authtoken')),  

    #second functionnality (menu-items endpoints)
    path('menu-items',views.menu_items),
    path('menu-items/<int:pk>',views.single_menu_item),
    path('api-token-auth',obtain_auth_token),

    #third functionality (user group management endpoints)
    #path('groups/manager/users',views.ManagerGroupView.as_view()),
    path('groups/manager/users',views.managers_post_get),
    path('groups/manager/users/<int:id>',views.delete_manager),

    path('groups/delivery-crew/users',views.delivery_crew_post_get),
    path('groups/delivery-crew/users/<int:id>',views.delete_delivery_member),

    #fourth functionnality (cart management endpoints)
    path('cart/menu-items',views.cart_management),
    
]





