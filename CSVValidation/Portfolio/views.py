from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist,FieldDoesNotExist
import csv
import os
import datetime
#from django.urls import request
from .models import Portfolio,Stuff
#from .forms import PortfolioForm
#from .forms import UploadFileForm
# Create your views here.

class Validating():
	def CSV_storing(user):
		usic = user
		el_list =[]
		PortList = Portfolio.objects.all()
		print(PortList)
		#print(dir(PortList))
		#for dat in Portfolio.objects.get(pk=4).data.all():
			#print(dir(dat))
		#print(el_list)
		for el in PortList:
				
			print(el.file)
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
						#print(header)
						if ('accountid' in header)  and ('date_opened' in header) and ('external_name'in header) :
							#print(str(el.file))
							Validating.Restoring(usic,el,str(el.file))
						else:
							Validating.Del(el,str(el.file))

		return('header')
	def Restoring(user,el,to_restore:str):
		usic=user
		rest_name = os.rename(str(to_restore) , 'stored/'+str(el.title)+'.csv')
		#print(rest_name	)
		rest_name = 'stored/' + str(el.title) + '.csv'
		el.file_stored = True
		el.filename = rest_name
		el.file.delete()
		el.save()
		Validating.Recording(usic,el)
		return('hello')
	def Del(el,to_delete:str):
		os.remove(to_delete)
		el.file.delete()
		el.file_stored = False
		el.save
		#print('nothere')
		return('bye')
	def Recording(user,el):
		res = dict()
		other_res = dict()
		observed_output = []
		header =[]	
		#print(el.filename)
		with open(str(el.filename), 'r') as csvfile:
					reader = csv.reader (csvfile, delimiter=',', quotechar='|')
					for row in reader:
						observed_output.append(row)
						header = observed_output[0]
						

					for i in range(1,len(observed_output)):
						res.update(zip(header,observed_output[i]))
						other_res.update(zip(header,observed_output[i]))
						print(other_res)
						other_res.pop('accountid')
						other_res.pop('date_opened')
						other_res.pop('external_name')
						#print(other_res)
						dat = Stuff(user=user,date = datetime.datetime.now(), accountid = res.get('accountid'), date_opened = res.get('date_opened'), external_name =  res.get('external_name'),others = other_res)
						dat.save()
						#print(res.get('accountid') )
						el.data.add(dat)
						el.save()
						el.data.add(dat)
		return('done')				

		

class PortfolioListView(ListView):				
	model = Portfolio
	template_name = 'home.html'
	def get(self, request: HttpRequest) -> HttpResponse:
		#print(request.method)
		try:
			user = request.user
			print('aloha')
			Validating.CSV_storing(user)
			PortList = Portfolio.objects.all()
			return (render(request,self.template_name,{'PortList':PortList}))

		except ObjectDoesNotExist:
				PortList = Portfolio.objects.all()
				return (render(request,self.template_name,{'PortList':PortList}))
		except FileNotFoundError:
				PortList = Portfolio.objects.all()
				return (render(request,self.template_name,{'PortList':PortList}))

		

class PortfolioCreateView(CreateView):
	model = Portfolio
	template_name = 'portfolio_new.html'
	fields = ['title','file']

class Success(ListView):
	model = Portfolio
	template_name = 'success.html'




class PortfolioDetailView(DetailView):
	def get(self, request: HttpRequest, pk: int) -> HttpResponse:
		z = Portfolio.objects.get(pk=pk)
		header = ['filename','user','date','accountid','date_opened','external_name',]
		data_list =[]
		other =[]
		print(z.data.all())
		for dat in z.data.all():
			data_list.append(dat)


		for el in data_list:
			print(el.others)
			for key in el.others.keys():
				#print(data_list)
				if key not in header:
					header.append(key)
				other.append(el.others.get(key))
		print(other)
		return(render(request,'portfolio_detail.html',{'portfolio':z,'data':data_list,'header':header,'other':other}))
