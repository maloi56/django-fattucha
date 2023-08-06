from django.contrib import admin

from users.models import EmailVerification, Tariff, User


@admin.register(User)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


@admin.register(EmailVerification)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'duration')
