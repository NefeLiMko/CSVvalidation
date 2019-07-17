from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist,FieldDoesNotExist
from django.shortcuts import redirect

import csv
import os
import datetime
#from django.urls import request
from .models import Portfolio,Stuff
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def CSV_storing(user):
		usic = user
		el_list =[]
		PortList = Portfolio.objects.all()
		for el in PortList:		
			observed_output = []
			header = []
			if el.file_stored == True or str(el.file)=='':
				pass
			else:			
				with open(str(el.file), 'r') as csvfile:
					reader = csv.reader (csvfile, delimiter=',', quotechar='|')
					for row in reader:
						observed_output.append(row)
						header = observed_output[0]
					if ('accountid' in header)  and ('date_opened' in header) and ('external_name'in header) :
						Restoring(usic,el,str(el.file))
					else:
						Del(el,str(el.file))

		return('header')


@shared_task
def Restoring(user,el,to_restore:str):
		usic=user
		el.num += 1

		rest_name = os.rename(str(to_restore) , 'stored/'+str(el.title) + '_' + str(el.num) +'.csv')
		rest_name = 'stored/'+str(el.title) + '_' + str(el.num) +'.csv'
		el.file_stored = True
		
		el.save()
		Recording(usic,el,rest_name)
		return('hello')

@shared_task
def Del(el,to_delete:str):
	os.remove(to_delete)
	el.file.delete()
	el.file_stored = False
	el.save
	return('bye')

@shared_task
def Recording(user,el,rest_name):
	res = dict()
	other_res = dict()
	observed_output = []
	header =[]	
	with open(str(rest_name), 'r') as csvfile:
				reader = csv.reader (csvfile, delimiter=',', quotechar='|')
				for row in reader:
					observed_output.append(row)
					header = observed_output[0]
					

				for i in range(1,len(observed_output)):
					res.update(zip(header,observed_output[i]))
					other_res.update(zip(header,observed_output[i]))
					other_res.pop('accountid')
					other_res.pop('date_opened')
					other_res.pop('external_name')
					dat = Stuff(status = "stored" ,filename = rest_name ,user=user,date = datetime.datetime.now(), accountid = res.get('accountid'), date_opened = res.get('date_opened'), external_name =  res.get('external_name'),others = other_res)
					dat.save()
					el.data.add(dat)
					el.save()
	el.save()
	Validation(el)
	return('done')				
@shared_task
def Validation(el):
	data_list =[]
	validation_list =[]
	for row in el.data.all():
		data_list.append(row)
	for row in data_list:
		if any(map(str.isdigit, str(row.external_name))) == True:
			row.status = "Invalid"
			row.save()
		else:
			if len(validation_list)!=0:
				for elem in validation_list:
					if (row.accountid==elem.accountid) and (row.date_opened== elem.date_opened) and (row.external_name==elem.external_name):
						row.status = "Invalid"
					else:
						row.status ="Valid"
						validation_list.append(row)
			else:
				row.status = "Valid"
				validation_list.append(row)
		row.save()
	return('hi')