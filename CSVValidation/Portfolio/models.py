from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse, reverse_lazy
from .checker import ContentTypeRestrictedFileField
# Create your models here.

class Stuff(models.Model):
	user = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now=False)
	accountid = models.IntegerField(default=0)
	date_opened = models.CharField(max_length=255)
	external_name = models.CharField(max_length=255)
	others = JSONField()
	class Meta:
		ordering = ('user','date', 'accountid','date_opened','external_name','others')
	def __str__(self):
					return self.external_name	





class Portfolio(models.Model):
	title = models.CharField(max_length=255,verbose_name="Title")
	file  = ContentTypeRestrictedFileField(upload_to='uploads/', content_types=['text/csv', ],max_upload_size=5242880 )
	status = models.CharField(max_length=255)
	file_stored = models.BooleanField(default=False)

	filename = models.CharField(max_length=255)
	data = models.ManyToManyField(Stuff, related_name="data",)
	

	def __str__(self):
		return self.title
	def file_path(self):
		return self.file
	def get_absolute_url(self):
		return reverse('port:success')