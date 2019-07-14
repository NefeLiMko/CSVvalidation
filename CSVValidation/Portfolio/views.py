from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView
from django.conf import settings
from .models import Portfolio
#from .forms import UploadFileForm
# Create your views here.


class PortfolioListView(ListView):
	model = Portfolio
	template_name = 'home.html'

class PortfolioCreateView(CreateView):
	model = Portfolio
	template_name = 'portfolio_new.html'
	fields = ['title','file',]

class PortfolioDetailView(DetailView):
	model = Portfolio
	template_name = 'portfolio_detail.html'
					