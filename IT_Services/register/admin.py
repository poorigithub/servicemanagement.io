from django.contrib import admin
from .models import Service,Subscription,login
# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','active']
    list_editable = ['active']


admin.site.register(Service,ServiceAdmin)
admin.site.register(Subscription)
admin.site.register(login)