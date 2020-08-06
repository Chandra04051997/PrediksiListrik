from django.contrib import admin
from .models import Article
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    
    fields = (
        'judul',
        'isi',
    )

admin.site.register(Article, ArticleAdmin)