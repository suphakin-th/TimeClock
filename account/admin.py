from django.contrib import admin

# Register your models here.
from account.models import Account, Clocking


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email'
    )
    

@admin.register(Clocking)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'clock_in',
        'clock_out',
        'datetime_update',
        'datetime_create'
    )