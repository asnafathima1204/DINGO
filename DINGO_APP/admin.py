from django.contrib import admin
from DINGO_APP.models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Chef)
admin.site.register(Reservation)
admin.site.register(Contact)