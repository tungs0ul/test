from django.contrib import admin
from .models import Room, Move, UserRecord

# Register your models here.
admin.site.register(Room)
admin.site.register(Move)
admin.site.register(UserRecord)
