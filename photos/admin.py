from django.contrib import admin

from .models import *


# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
	list_display = ('album', 'location', 'user', 'title', 'description', 'upload_date', 'img')


class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'latitude', 'longitude')


class AlbumAdmin(admin.ModelAdmin):
	list_display = ('description',)


class TagAdmin(admin.ModelAdmin):
	list_display = ('description',)


class PhotoTagAdmin(admin.ModelAdmin):
	list_display = ('photo', 'tag',)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('album', 'content')


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(Comment, CommentAdmin)
