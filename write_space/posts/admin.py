from django.contrib import admin
from . import models
from mptt.admin import DraggableMPTTAdmin
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)
    class Media:
        js = ('http://code.jquery.com/jquery-3.1.1.js',
        'https://widget.cloudinary.com/v2.0/global/all.js','write_space/js/main.js',)

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Cartegory, DraggableMPTTAdmin )
