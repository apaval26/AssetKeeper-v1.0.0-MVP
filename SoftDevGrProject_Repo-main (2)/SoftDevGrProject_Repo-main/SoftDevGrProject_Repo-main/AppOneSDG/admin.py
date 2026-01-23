from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Equipment, Device_Serial_Number, Admin, Reservation, Admin_User_Manage, Admin_Equip_Manage   #from .models import User

# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('userId', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, MyUserAdmin)
admin.site.register(Equipment)
admin.site.register(Device_Serial_Number)
admin.site.register(Admin)
admin.site.register(Reservation)
admin.site.register(Admin_User_Manage)
admin.site.register(Admin_Equip_Manage)