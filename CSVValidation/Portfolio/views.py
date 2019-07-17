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
		user = request.user
		CSV_storing.delay(str(user))
		PortfolioList = Portfolio.objects.all()
		return (render(request,self.template_name,{'PortList':PortfolioList}))


		

class PortfolioCreateView(CreateView):
	model = Portfolio
	template_name = 'portfolio_new.html'
	fields = ['title','file']


class PortfolioUpdateView(UpdateView):
	model = Portfolio
	template_name = 'portfolio_edit.html'
	fields = ['file']	
	reverse_lazy('port:home')
	def post(self, request: HttpRequest, pk: int) -> HttpResponse:
		portfolio = Portfolio.objects.get(pk=pk)
		portfolio.file = request.FILES.get('file')
		portfolio.file_stored = False
		portfolio.validating = False
		portfolio.save()
		return( HttpResponseRedirect('/'))	

class PortfolioDeleteView(DeleteView):
	model = Portfolio
	template_name="portfolio_delete.html"
	success_url = reverse_lazy('port:home')

class PortfolioDetailView(DetailView):
	def get(self, request: HttpRequest, pk: int) -> HttpResponse:

		portfolio = Portfolio.objects.get(pk=pk)
		header = ['filename','user','date','accountid','date_opened','external_name',]
		data_list =[]
		other_fields = []

		for data in portfolio.data.all():
			data_list.append(data)
				
		for el in data_list:
			if el.others!=True :
				for key in el.others.keys():
					if key not in header:
						header.append(key)
					other_fields.append(el.others.get(key))
		for el in data_list:
			for key in header[6:]:
				if key not in el.others.keys():
					el.others.update({key:'none'})	
					el.save()		
		Validation(portfolio)
		messages.success(self.request, 'Validation is in progress! Wait a moment and refresh this page.')
		return(render(request,'portfolio_detail.html',{'portfolio':portfolio,'data':data_list,'header':header,}))
