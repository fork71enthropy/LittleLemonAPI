from rest_framework import serializers
from .models import MenuItem
from django.contrib.auth.models import User





class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category'] #
        extra_kwargs = {
            
        }
        read_only_fields = ['id']
#C'est incroyable, il faut que je révise les notions sur les serializers

class ManagerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email'] # C'est pour tester
        read_only_fields = ['id']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','username','email'] # C'est pour tester



















