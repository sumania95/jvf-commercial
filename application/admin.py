from django.contrib import admin

from .models import (
    Product,
    Brand,
    Branch,
    User_Type,
)


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Branch)
admin.site.register(User_Type)
