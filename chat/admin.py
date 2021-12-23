from django.contrib import admin
from . models import Live_User,Room,Messages,Subscriptions

# Register your models here.

@admin.register(Live_User)
class Live_UserAdmin(admin.ModelAdmin):
	list_display = ('user_id','uniq_userid','user')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('room_id','name')

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id','lu_ref', 'room_ref')

@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('lu_ref', 'room_ref')
