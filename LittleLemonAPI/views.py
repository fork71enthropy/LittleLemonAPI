from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser  
from django.contrib.auth.models import User,Group
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer



#from rest_framework import status
# Create your views here.
"""

 People with different roles will be able to browse, add and edit menu items,
   place orders, browse orders, assign delivery crew 
   to orders and finally deliver the orders. 

"""

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


#Je ne sais pas si j'ai terminé les fonctionnalités de vues pour les menu-items, 
#J'avais réussi les vues menu-items, je ne sais pas ce que je dois rajouter
#il est 00:42, j'ai déjà écrit les bases pour les vues menu-items, c'est bien,
#je dois rajouter les logiques d'authorisation en fonction du User group
#revoir la vidéo sur les users roles









