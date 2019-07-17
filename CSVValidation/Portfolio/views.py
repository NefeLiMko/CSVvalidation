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
from .tasks import Recording,Restoring,Del,CSV_storing,Validation
#from .forms import PortfolioForm
#from .forms import UploadFileForm
# Create your views here.


	
	

		

class PortfolioListView(ListView):				
	model = Portfolio
	template_name = 'home.html'
	def get(self, request: HttpRequest) -> HttpResponse:
		try:
			user = request.user
			CSV_storing.delay(str(user))
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

class PortfolioUpdateView(UpdateView):
	model =Portfolio
	template_name = 'portfolio_edit.html'
	fields =['file']	
	reverse_lazy('port:success')
	def post(self, request, pk: int) :
		Port = Portfolio.objects.get(pk=pk)
		Port.file = request.FILES.get('file')
		Port.file_stored = False
		Port.save()
		return( HttpResponseRedirect('/success/'))	

class PortfolioDeleteView(DeleteView):
	model = Portfolio
	template_name="portfolio_delete.html"
	success_url = reverse_lazy('port:home')

class PortfolioDetailView(DetailView):
	def get(self, request: HttpRequest, pk: int) -> HttpResponse:

		z = Portfolio.objects.get(pk=pk)
		header = ['filename','user','date','accountid','date_opened','external_name',]
		data_list =[]
		other = []
		oth = dict()

		for dat in z.data.all():
			data_list.append(dat)
				
		for el in data_list:
			if el.others!=True :
				for key in el.others.keys():
					if key not in header:
						header.append(key)
					other.append(el.others.get(key))
		for el in data_list:
			for key in header[6:]:
				if key not in el.others.keys():
					el.others.update({key:'none'})	
					el.save()		

		return(render(request,'portfolio_detail.html',{'portfolio':z,'data':data_list,'header':header,}))
