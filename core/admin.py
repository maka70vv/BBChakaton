from django.contrib import admin
from .models import Post, TendersList


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)


class ParserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TendersList, ParserAdmin)
