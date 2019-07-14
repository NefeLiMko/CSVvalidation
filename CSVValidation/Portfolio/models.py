from django.db import models
from django.urls import reverse, reverse_lazy
from .checker import ContentTypeRestrictedFileField
# Create your models here.

class Stuff(models.Model):
    title = models.CharField(max_length=245)
    

class Portfolio(models.Model):
	title = models.CharField(max_length=60,verbose_name="Title")
	file  = ContentTypeRestrictedFileField(upload_to='uploads/', content_types=['text/csv', ],max_upload_size=5242880, )
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home', )