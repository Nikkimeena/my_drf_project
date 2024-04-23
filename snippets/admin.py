from django.contrib import admin
from snippets.models import Snippet



class SnippetAdmin(admin.ModelAdmin):
    list_display=['created','tittle','code','linenos','language','style']


admin.site.register(Snippet,SnippetAdmin)
