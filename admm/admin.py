from django.contrib import admin
from .models import Advertisement,Area,City,State,Country,Category,Subcategory,Userrole
from django.apps import apps
# Register your models here.

# mdls = apps.get_app_config('admm').get_models()
# for mdl in mdls:
#     admin.site.register(mdl)


admin.site.register(Area)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Subcategory)
# admin.site.register(Userdetail)
admin.site.register(Userrole)