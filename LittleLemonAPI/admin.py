from django.contrib import admin
from .models import Category
from .models import MenuItem
from .models import CartItem
from .models import Order
from .models import OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)



#update: je suis sur la partie Menu-items endpoints, il est 00h12, 
#je dois écrire tous ces endpoints