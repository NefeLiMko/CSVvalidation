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
		el_list =[]
		PortfolioList = Portfolio.objects.all()
		for el in PortfolioList:		
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
						Restoring(user,el,str(el.file))
					else:
						Del(el,str(el.file))

		pass


@shared_task
def Restoring(user,el,to_restore:str):
	el.num += 1

	rest_name = os.rename(str(to_restore) , 'stored/'+str(el.title) + '_' + str(el.num) +'.csv')
	rest_name = 'stored/'+str(el.title) + '_' + str(el.num) +'.csv'
	el.file_stored = True	
	el.save()
	Recording(user,el,rest_name)
	pass

@shared_task
def Del(el,to_delete:str):
	os.remove(to_delete)
	el.file.delete()
	el.file_stored = False
	el.save
	pass

@shared_task
def Recording(user,el,rest_name):
	result = dict()
	other_result = dict()
	observed_output = []
	header =[]	
	with open(str(rest_name), 'r') as csvfile:
				reader = csv.reader (csvfile, delimiter=',', quotechar='|')
				for row in reader:
					observed_output.append(row)
					header = observed_output[0]
					
				try:
					for i in range(1,len(observed_output)):
						result.update(zip(header,observed_output[i]))
						other_result.update(zip(header,observed_output[i]))
						other_result.pop('accountid')
						other_result.pop('date_opened')
						other_result.pop('external_name')
						data = Stuff(status = "stored" ,filename = rest_name ,user=user,date = datetime.datetime.now(), accountid = res.get('accountid'), date_opened = res.get('date_opened'), external_name =  res.get('external_name'),others = other_res)
						data.save()
						el.data.add(data)
						el.save()

				except ValueError as e:
					pass
	el.save()
	Validation(el)
	pass			
@shared_task
def Validation(el):
	if el.validating == True:
		return 'validated'
	data_list =[]
	validation_list =[]
	for row in el.data.all():
		data_list.append(row)
	for row in data_list:
		print(row.accountid, row.date_opened, row.external_name)
		if (str(row.accountid)!='') and (str(row.date_opened)!='') and (str(row.external_name)!=''): 
			if any(map(str.isdigit, str(row.external_name))) == True:
				row.status = "Invalid"
			else:
				print(len(data_list))
				print(len(validation_list))
				if len(validation_list)!=0:
					for elem in validation_list:
						if (row.accountid==elem.accountid) and (row.date_opened== elem.date_opened) and (row.external_name==elem.external_name):
							row.status = "Invalid"
							break
						else:
							row.status ="Valid"
					if row.status == "Valid":
						validation_list.append(row)						
				else:
					row.status = "Valid"
					validation_list.append(row)
					
		else:
			row.status = "Invalid"
		row.save()
		el.validating = True
		el.save()
	return 'validation successfull'