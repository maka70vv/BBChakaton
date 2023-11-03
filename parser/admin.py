from django.contrib import admin

from parser.models import TendersList


# Register your models here.
class ParserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TendersList, ParserAdmin)