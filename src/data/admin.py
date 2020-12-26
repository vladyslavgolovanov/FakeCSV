from django.contrib import admin

# Register your models here.
from data.models import Schemas, Column, File

admin.site.register(Schemas)
admin.site.register(Column)
admin.site.register(File)
