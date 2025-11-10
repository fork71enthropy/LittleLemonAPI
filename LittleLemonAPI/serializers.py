from rest_framework import serializers
from .models import MenuItem



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']
        extra_kwargs = {
            
        }
#C'est incroyable, il faut que je révise les notions sur les serializers
