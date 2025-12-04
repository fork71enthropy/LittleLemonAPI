from rest_framework import serializers
from .models import MenuItem,CartItem,Order,OrderItem
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

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['user','menuitem','quantity','unit_price','price']
        read_only_fields = ['id', 'user', 'unit_price', 'price', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order','menuitem','quantity','unit_price','price']


class OrderSerializer(serializers.ModelSerializer):
    #on récupère tous les orderItem liés à l'order
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order 
        fields = ['user','delivery_crew','status','total','date','order_items']
        read_only_fields = ['user', 'total', 'date', 'order_items']

#Donc inutile
class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        #fields = [f'{model.menuitem.title}']
        fields = ['menuitem']
        
    def create(self, validated_data):
        #Pour vérifier que cet utilisateur a bien l'item dans son panier/cart avant validation
        #if(OrderItem.order == CartItem.user and OrderItem.menuitem == CartItem.menuitem):
        request = self.context['request']
        order = request.order
        menuitem = validated_data['menuitem']
        quantity = 1  # par défaut
        # exemple : vérifier qu'il y a bien l'item dans le cart,attention, ici order est supposé être égal
        #à user, donc ca passe !
        exists = CartItem.objects.filter(order=order, menuitem=menuitem).exists()
        if not exists:
            raise serializers.ValidationError(
                {"detail": "This item is not in your cart."}
            )

        order_item, created = OrderItem.objects.get_or_create(
            order = order,
            menuitem = menuitem,
            defaults={
                'quantity': quantity,
                'unit_price': menuitem.price,
                'price': menuitem.price * quantity,
            },
        )

        if not created:
            # si l'item existe déjà, on incrémente la quantité
            order_item.quantity = order_item.quantity + quantity
            order_item.price = order_item.quantity * order_item.unit_price
            order_item.save()
        return order_item




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













#J'aime beaucoup tout ce qu'on peut faire avec les serializers !