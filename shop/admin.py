from django.contrib import admin
from .models import * 

"""class CategoryAdmin(admin.ModelAdmin):
    listDisplay = ("name",'image','descripition')
    admin.site.register(Catageory,CategoryAdmin)
    """
    
admin.site.register(Catageory)
admin.site.register(Product)