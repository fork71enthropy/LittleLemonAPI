# permissions.py
from rest_framework.permissions import BasePermission

class IsManagerForModification(BasePermission):
    """
    Permission personnalisée qui autorise uniquement les managers 
    à créer, modifier ou supprimer des ressources.
    """
    def has_permission(self, request, view):
        # Les méthodes de lecture sont autorisées pour tous
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Les méthodes de modification nécessitent d'être manager
        return request.user.groups.filter(name="manager").exists()
    

    #10/11/2025
    #18h05

    #update, j'ai réussi la première fonctionnalité, je suis vraiment fier de moi car 
    #je l'ai trouvé tout seul, j'adore la prouesse intellectuelle, je kiffe ca. Demain 
    #si je termine rapidement les mathématiques je pourrai reprendre sur le projet en 
    #question et terminer le reste des fonctionnalités d'authorization avec menu-item
    #Le rythme est bon, enfin un truc positif dans la journée ! A plus tard, je pousse 
    #le code et je m'en vais dormir, je dois plus rapide la prochaine fois, et ensuite 
    #on ira de plus en plus vite, je serai aussi fort voir plus fort que les seniors, 
    #je connais normalement en 3 ans je devrais devenir monstrueux ! Là on commence à être 
    #vraiment bon !