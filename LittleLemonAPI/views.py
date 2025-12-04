#pour les menu items endpoints
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group,User
from .models import MenuItem,CartItem
from .serializers import MenuItemSerializer
#j'importe les classes de permissions et pour les views functions, ca m'énerve de devoir changer de style de 
#programmation pour ces nouvelles fonctionnalités
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from .serializers import ManagerGroupSerializer,CustomUserSerializer,CartItemSerializer,CartItemCreateSerializer
 



#from rest_framework import status
# Create your views here.
# Voilà, c'est dans la vue que je devais gérer les authorisations, ca m'énerve.
# La prochaine fois je mettrai moins de temps à comprendre ca
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # tout le monde doit être loggé
def menu_items(request):
    """
    /api/menu-items/

    - GET  : Customer, Delivery crew, Manager
    - POST : Manager uniquement (sinon 403)
    """

    # GET : tous les users authentifiés
    if request.method == 'GET':
        items = MenuItem.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST : réservé aux Managers
    is_manager = request.user.groups.filter(name="Manager").exists()
    if not is_manager:
        return Response(
            {"detail": "You must be a Manager to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])  # tout le monde doit être loggé
def single_menu_item(request, pk):
    """
    /api/menu-items/<pk>/

    - GET          : Customer, Delivery crew, Manager
    - PUT/PATCH/DELETE : Manager uniquement (sinon 403)
    """

    try:
        item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(
            {"detail": "Menu item not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # GET : tout user authentifié
    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # méthodes sensibles : Manager only
    is_manager = request.user.groups.filter(name="Manager").exists()
    if not is_manager:
        return Response(
            {"detail": "You must be a Manager to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = MenuItemSerializer(
            item, data=request.data, partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#La réponse était dans une vidéo carrément, j'ai honte
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def managers_post_get(request):
    """
    Endpoint pour ajouter un utilisateur au groupe des managers
    """
    # POST et GET : réservé aux Managers
    is_manager = request.user.groups.filter(name="manager").exists()
    if not is_manager:
        return Response(
            {"detail": "You must be a Manager to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
    
    if request.method == 'GET':
        managers = User.objects.filter(groups__name="manager")
        serializer = ManagerGroupSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #pour le payload; c'est long et fatiguant à lire comme code putain
    username = request.data.get("username")
    if username:
        user = get_object_or_404(User,username = username)
        managers = Group.objects.get(name="manager")
        if request.method == 'POST':
            managers.user_set.add(user)

        return Response({"message":f"{username} was successfully added to the manager team"})
    return Response({"error":"hahahaha"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_manager(request,id):
    #DELETE réservé uniquement à un manager pour retirer un autre manager du groupe
    # 1) Seul un manager peut retirer un autre manager
    is_manager = request.user.groups.filter(name="manager").exists()
    if not is_manager:
        return Response({"detail": "You must be a Manager to perform this action."},
                        status=status.HTTP_403_FORBIDDEN,)
    
    # 2) Récupérer le user ciblé, qui doit être dans le groupe manager
    user = get_object_or_404(User, id=id, groups__name="manager")

    # 3) Récupérer le groupe manager
    manager_group = get_object_or_404(Group, name="manager")

    # 4) Retirer le user du groupe
    manager_group.user_set.remove(user)

    return Response(
        {"message": f"{user.username} was successfully removed from manager group."},
        status=status.HTTP_200_OK,
    )

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew_post_get(request):
    """ 
    GET return all the delivery crew
    POST assign the payload to the delivery crew group
    """
    # 1) Seul un manager peut voir les membres du delivery crew
    is_manager = request.user.groups.filter(name="manager").exists()
    if not is_manager:
        return Response({"detail": "You must be a Manager to perform this action."},
                        status=status.HTTP_403_FORBIDDEN,)

    if request.method == 'GET':
        delivery_crew = User.objects.filter(groups__name="delivery_crew")
        serializer = CustomUserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    #pour le payload; c'est long et fatiguant à lire comme code putain
    username = request.data.get("username")
    if username:
        user = get_object_or_404(User,username = username)
        delivery_crew = Group.objects.get(name="delivery_crew")
        if request.method == 'POST':
            delivery_crew.user_set.add(user)

        return Response({"message":f"{username} was successfully added to the delivery crew"})
    return Response({"error":"hahahaha"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_delivery_member(request,id):
    """
    DELETE comme pour le delete des managers
    """
    # 1) Seul un manager peut retirer un autre manager
    is_manager = request.user.groups.filter(name="manager").exists()
    if not is_manager:
        return Response({"detail": "You must be a Manager to perform this action."},
                        status=status.HTTP_403_FORBIDDEN,)
    
    try:
        # 2) Récupérer le user ciblé, qui doit être dans le groupe delivery_crew
        user = get_object_or_404(User, id=id, groups__name="delivery_crew")
        """
            if not user :

        """


        # 3) Récupérer le groupe manager
        delivery_crew = get_object_or_404(Group, name="delivery_crew")
        

        # 4) Retirer le user du groupe
        delivery_crew.user_set.remove(user)

        return Response(
            {"message": f"{user.username} was successfully removed from the delivery crew."},
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"detail": f"User with id {id} is not in the delivery crew group."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    except Exception as e:
        return Response(
            {"detail": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
"""
9h58
03/12/2025: UserGroup Management endpoints est terminé, maintenant je dois modifier quelques lignes
pour pouvoir obtenir les messages de sorties que je veux !

A faire à 17h30 le 03/12/2025
Cart Management Endpoints à écrire; ca m'a l'air vraiment facile à faire 
"""

"""
GET : return current items in the cart for the current token of the user
"""
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart_management(request):
    """
    api/cart/menu-items
    GET : Returns current items in the cart for the current user token
    POST : Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items
    """ 
    #2)
    if request.method == 'GET':
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #fonctionnalité POST
    if request.method == 'POST':
        serializer = CartItemCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            menuitem_id = cart_item.menuitem.id 
            return Response( f"Item {menuitem_id} successfully added", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #fonctionnalité DELETE
    if request.method == 'DELETE':
        try:
            items = CartItem.objects.filter(user=request.user)
            items.delete()
            return Response( {"detail":"all items were successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Cart Items not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response({"message":"Ca pue la merde, tu devrais vérifier ce que tu as écrit"})



#revoir la vidéo sur les users roles
#Il faut que je prenne plus de risques lorsque je code ! Essais des choses, c'est comme ca qu'on apprend

"""
Dernière fonctionnalité, les endpoints pour les orders des clients, ca m'a l'air facile.
A faire le 04/12/2025 à 15h30
"""
 






"""
19h53, 01/12/2025, j'ai enfin terminé la première partie
C'est un truc de fou que le mois soit en train de se terminer ! Je viens de terminer les 
menu-items endpoints avec les permissions correspondantes.
"""
"""
Je passe aux User group management endpoints maintenant !
"""

 


 
 