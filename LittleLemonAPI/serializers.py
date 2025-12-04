from rest_framework import serializers
from .models import MenuItem
from django.contrib.auth.models import User
from .models import CartItem





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

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['user','menuitem','quantity','unit_price','price']
        read_only_fields = ['id', 'user', 'unit_price', 'price', 'created_at']



class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['menuitem'] #on aura besoin que du menuitem dans le payload

    def create(self, validated_data):
        request = self.context['request'] # ← KeyError ici
        user = request.user
        menuitem = validated_data['menuitem']

        quantity = 1  # par défaut

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            menuitem=menuitem,
            defaults={
                'quantity': quantity,
                'unit_price': menuitem.price,
                'price': menuitem.price * quantity,
            },
        )

        if not created:
            # si l'item existe déjà, on incrémente la quantité
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.price = cart_item.quantity * cart_item.unit_price
            cart_item.save()
        return cart_item













