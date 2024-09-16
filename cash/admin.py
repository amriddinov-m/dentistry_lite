from django.contrib import admin

from cash.models import Cash, CashLog


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    pass


@admin.register(CashLog)
class CashLogAdmin(admin.ModelAdmin):
    pass
