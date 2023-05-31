from django.db.models import Count

from .models import *
from django.db import connection
from quiz_site.settings import MEDIA_URL
menu = [{'title': "Главное", 'url_name': 'home'},
		{'title': "Добавить альбом", 'url_name': 'add_album'},
		{'title': "Добавить фото", 'url_name': 'add_photo'},
]

class DataMixin:
	def get_photos_context(self, **kwargs):
		context = {'posts': [], 'menu': menu}
		for i in kwargs['posts']:
			album_id = i['id']
			with connection.cursor() as cursor:
				cursor.execute("""SELECT img FROM photos_photo WHERE album_id = %s""", [album_id, ])
				row = cursor.fetchone()

			if row is not None:
				i['photo'] = MEDIA_URL + row[0]
			context['posts'].append(i)
		return context

	def get_menu_context(self, **kwargs):
		context = kwargs
		context['menu'] = menu
		return context
