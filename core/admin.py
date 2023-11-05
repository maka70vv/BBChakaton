from django.contrib import admin
from .models import TendersList, ContractsList


class ParserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TendersList, ParserAdmin)
admin.site.register(ContractsList, ParserAdmin)
