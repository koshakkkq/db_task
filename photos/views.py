import datetime
import hashlib
import os
import random
from datetime import date

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.core.files.storage import default_storage, FileSystemStorage
from django.views.generic.edit import FormMixin
from quiz_site.settings import MEDIA_URL, MEDIA_ROOT
from django.db import connection

# Create your views here.
from .utils import *
from .models import *
from .forms import *


def index(request):
	return HttpResponse('Начальная страница.')


class Albums(DataMixin, ListView):
	model = Album
	template_name = 'photos/index.html'
	context_object_name = 'posts'
	allow_empty = False

	def get_posts_raw_sql(self):
		with connection.cursor() as cursor:
			query = """SELECT * FROM photos_album"""
			cursor.execute(query)
			rows = cursor.fetchall()
			posts = []

			for row in rows:
				posts.append({'id':row[0], 'description':row[1]})
			return posts
	def get_context_data(self, *, object_list=None, **kwargs):
		albums = self.get_posts_raw_sql()
		context = self.get_photos_context(posts=albums)
		c_def = self.get_menu_context(title='Меню')
		context = dict(list(context.items()) + list(c_def.items()))
		return context



class PhotoView(LoginRequiredMixin, DataMixin, ListView, ):
	template_name = 'photos/photos.html'
	model = Photo
	context_object_name = 'photos'
	login_url = reverse_lazy('login')

	def get_comments(self, album_id):

		with connection.cursor() as cursor:
			query = """SELECT auth_user.username, photos_comment.content FROM photos_comment 
			LEFT JOIN auth_user
			ON auth_user.id = photos_comment.user_id
            WHERE photos_comment.album_id = %s;
			"""
			cursor.execute(query, [album_id])
			rows = cursor.fetchall()
			comments = []

			for row in rows:
				comments.append({'content': row[1],'user':row[0]})
			return comments

	def get_photo_dict(self, req_arr):
		res = {
			'username': req_arr[0],
			'title': req_arr[1],
			'description': req_arr[2],
			'post_date': req_arr[3],
			'img': MEDIA_URL + req_arr[4],
			'location': req_arr[5],
		}
		return res

	def get_photos(self, album_id):
		query = """
		SELECT auth_user.username,
		photo.title, photo.description, photo.upload_date, photo.img,
		photos_location.name
		FROM photos_photo photo
		LEFT JOIN auth_user
			ON auth_user.id = photo.user_id
		INNER JOIN photos_location
			ON photos_location.id = photo.location_id
		WHERE photo.album_id = %s;
					"""

		with connection.cursor() as cursor:
			cursor.execute(query, [album_id])
			rows = cursor.fetchall()
			res = []
			for i in rows:
				res.append(self.get_photo_dict(i))
			return res
	def get_context_data(self, **kwargs):
		c_def = self.get_menu_context(title='Альбом')
		c_def['comments'] = self.get_comments(self.kwargs['album_id'])
		c_def['album_id'] = self.kwargs['album_id']
		c_def['photos'] = self.get_photos(self.kwargs['album_id'])
		return c_def

	def get_queryset(self):
		album_id = self.kwargs['album_id']
		return Photo.objects.filter(album__id=album_id)



	def get_success_url(self):
		return reverse_lazy('album', kwargs={'album_id': self.kwargs['album_id']})

	def post(self, request, *args, **kwargs):
		content = request.POST.get('content')
		user_id = request.user.id
		album_id = self.kwargs['album_id']
		query = """INSERT INTO photos_comment (content, album_id, user_id) values (%s, %s, %s)"""
		with connection.cursor() as cursor:
			cursor.execute(query, [content, album_id, user_id])
		return HttpResponseRedirect(self.get_success_url())


class AddAlbum(LoginRequiredMixin, DataMixin, TemplateView):
	template_name = 'photos/add_album.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('login')
	#raise_exception = True

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Добавить альбом')
		c_def['post_url'] = 'add_album'
		return dict(list(context.items()) + list(c_def.items()))

	def get_success_url(self):
		return reverse_lazy('home')

	def post(self, request, *args, **kwargs):
		description = request.POST.get('description')
		query = """INSERT INTO photos_album (description) values (%s)"""
		with connection.cursor() as cursor:
			cursor.execute(query, [description])
		return HttpResponseRedirect(self.get_success_url())

class AddPhoto(LoginRequiredMixin, DataMixin, TemplateView):
	template_name = 'photos/add_photo.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('login')
	#raise_exception = False

	def get_locations(self):
		with connection.cursor() as cursor:
			query = """SELECT id, name FROM photos_location"""
			cursor.execute(query)
			rows = cursor.fetchall()
			locations = []

			for row in rows:
				locations.append({'id': row[0], 'name': row[1]})
			return locations


	def get_albums(self):
		with connection.cursor() as cursor:
			query = """SELECT id, description FROM photos_album"""
			cursor.execute(query)
			rows = cursor.fetchall()
			albums = []

			for row in rows:
				albums.append({'id': row[0], 'description': row[1]})
			return albums
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Добавить фото')
		c_def['post_url'] = 'add_photo'
		c_def['albums'] = self.get_albums()
		c_def['locations'] = self.get_locations()
		return dict(list(context.items()) + list(c_def.items()))

	def get_success_url(self):
		return reverse_lazy('home')


	def save_photo(self, file):
		today = datetime.datetime.now()
		today_path = today.strftime("%Y/%m/%d")
		ext = file.name.split('.')[-1]
		file.name = str(random.random()) + file.name + str(random.random())
		hash = hashlib.sha1(file.name.encode('UTF-16')).hexdigest()
		file.name = hash[:10]
		path = MEDIA_ROOT+'/photos/' + today_path+ '/' + file.name + '.' + ext
		default_storage.save(path, file)
		file_path = 'photos/' + today_path+ '/' + file.name + '.' + ext
		return file_path

	def post(self, request, *args, **kwargs):
		description = request.POST.get('description')[0]
		title = request.POST.get('title')[0]
		upload_date = datetime.datetime.now()
		req_file = request.FILES['img']
		img = self.save_photo(req_file)
		album_id = request.POST.get('album')[0]
		location_id = request.POST.get('location')[0]
		user_id = request.user.id

		query = """INSERT INTO photos_photo (title, description, upload_date, img, album_id, location_id, user_id) 
		values (%s, %s, %s, %s, %s, %s, %s)"""
		with connection.cursor() as cursor:
		 	cursor.execute(query, [title, description, upload_date, img, album_id, location_id, user_id])
		return HttpResponseRedirect(self.get_success_url())


class RegisterUser(DataMixin, CreateView):
	form_class = RegisterUserForm
	template_name = 'photos/register.html'
	success_url = reverse_lazy('login')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Регистрация')
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')


class LoginUser(DataMixin, LoginView):
	form_class = LoginUserForm
	template_name = 'photos/login.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Авторизация')
		return dict(list(context.items()) + list(c_def.items()))

	def get_success_url(self):
		return reverse_lazy('home')


def logout_user(requset):
	logout(requset)
	return redirect('login')
