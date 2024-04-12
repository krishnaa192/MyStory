from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Story)
admin.site.register(Part)
admin.site.register(CreatePlaylist)