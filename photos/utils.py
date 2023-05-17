from django.db.models import Count

from .models import *


menu = [{'title': "Главное", 'url_name': 'home'},
		{'title': "Добавить альбом", 'url_name': 'add_album'},
		{'title': "Добавить фото", 'url_name': 'add_photo'},
]

class DataMixin:
	def get_photos_context(self, **kwargs):
		context = {'posts': [], 'menu': menu}
		for i in kwargs['posts']:


			photo = Photo.objects.filter(album=i.pk)[:1]

			if len(photo) != 0:
				i.photo = photo[0].img

			context['posts'].append(i)
		return context

	def get_menu_context(self, **kwargs):
		context = kwargs
		context['menu'] = menu
		return context
