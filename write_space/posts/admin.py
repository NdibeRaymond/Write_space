from django.contrib import admin
from . import models
from mptt.admin import DraggableMPTTAdmin

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Cartegory, DraggableMPTTAdmin )
