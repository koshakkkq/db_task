from django.db import models
from django.contrib.auth import settings
from django.urls import reverse


# Create your models here.

class Photo(models.Model):
	album = models.ForeignKey('Album', on_delete=models.PROTECT)
	location = models.ForeignKey('Location', on_delete=models.PROTECT)
	user = models.ForeignKey('auth.User', on_delete=models.PROTECT)

	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	upload_date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(upload_to="photos/%Y/%m/%d/")

	def __str__(self):
		return self.title

class Album(models.Model):
	description = models.CharField(max_length=255)

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('album', kwargs={'album_id':self.pk})

class Location(models.Model):
	name = models.CharField(max_length=255)
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __str__(self):
		return self.name
class Tag(models.Model):
	description = models.CharField(max_length=255)

	def __str__(self):
		return self.description
class PhotoTag(models.Model):
	photo = models.ForeignKey('Photo', on_delete=models.PROTECT)
	tag = models.ForeignKey('Tag', on_delete=models.PROTECT)


class Comment(models.Model):
	album = models.ForeignKey('album', on_delete=models.PROTECT)
	content = models.CharField(max_length=255)
	user = models.ForeignKey('auth.User', on_delete=models.PROTECT, default=1)

