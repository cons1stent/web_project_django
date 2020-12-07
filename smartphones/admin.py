from django.contrib import admin

from .models import Smartphone, Sale


class SmartphoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'storage', 'cost', 'brand')


class SalesAdmin(admin.ModelAdmin):
    list_display = ('smartphone', 'created_at')


admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Sale, SalesAdmin)