from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser  
from django.contrib.auth.models import User,Group
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsManagerForModification


#from rest_framework import status
# Create your views here.
# Voilà, c'est dans la vue que je devais gérer les authorisations, ca m'énerve.
# La prochaine fois je mettrai moins de temps à comprendre ca

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated,IsManagerForModification]
   

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
   


#revoir la vidéo sur les users roles
#10/11/2025, 13h25




"""

 People with different roles will be able to browse, add and edit menu items,
   place orders, browse orders, assign delivery crew 
   to orders and finally deliver the orders. 

"""


"""    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # Allow only managers
            if not self.request.user.groups.filter(name="manager").exists():
                return Response({"message":"Only managers are authorized"},
                                status=status.HTTP_403_FORBIDDEN)
            return super().get_permissions()"""