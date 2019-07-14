from django.urls import path
from .views import PortfolioListView,PortfolioCreateView,PortfolioDetailView
urlpatterns = [
	path('portfolio/new/', PortfolioCreateView.as_view(), name="portfolio_new"),
	path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name ="portfolio_detail"),
	path('', PortfolioListView.as_view(), name = 'home'),
]