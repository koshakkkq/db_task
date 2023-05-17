from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormMixin

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

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context = self.get_photos_context(posts=context['posts'])
		c_def = self.get_menu_context(title='Меню')
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class PhotoView(DataMixin, FormMixin, ListView):
	template_name = 'photos/photos.html'
	model = Photo
	context_object_name = 'photos'
	form_class = AddCommentForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Альбом')
		c_def['comments'] = Comment.objects.filter(album__id=self.kwargs['album_id'])
		c_def['album_id'] = self.kwargs['album_id']
		return dict(list(context.items()) + list(c_def.items()))

	def get_queryset(self):
		album_id = self.kwargs['album_id']
		return Photo.objects.filter(album__id=album_id)

	def form_valid(self, form):
		form.instance.album = Album.objects.get(pk=self.kwargs['album_id'])
		form.save()
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('album', kwargs={'album_id': self.kwargs['album_id']})

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)



class AddAlbum(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddAlbumForm
	template_name = 'photos/addpage.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('login')
	raise_exception = True

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Добавить альбом')
		c_def['post_url'] = 'add_album'
		return dict(list(context.items()) + list(c_def.items()))


class AddPhoto(LoginRequiredMixin, DataMixin, CreateView):
	form_class = AddPhotoForm
	template_name = 'photos/addpage.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('login')
	raise_exception = True

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		c_def = self.get_menu_context(title='Добавить фото')
		c_def['post_url'] = 'add_photo'
		return dict(list(context.items()) + list(c_def.items()))

	def form_valid(self, form):
		form.instance.user = User.objects.get(pk=self.request.user.id)
		return super().form_valid(form)


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
