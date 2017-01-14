from django.contrib import admin

from mutual_funds.finance.models import Fund

from .models import ManagementCompany


class FundInline(admin.StackedInline):
    model = Fund
    extra = 0
    classes = ('grp-collapse',)

    def has_add_permission(self, request):
        return False


@admin.register(ManagementCompany)
class ManagementCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FundInline]
