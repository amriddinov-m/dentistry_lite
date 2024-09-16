from django.contrib import admin

from company.models import Company, Branch


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    pass
