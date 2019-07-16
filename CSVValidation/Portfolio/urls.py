from django.urls import path
from .views import PortfolioListView,PortfolioCreateView,PortfolioDetailView,Success

app_name = 'port'

urlpatterns = [
	path('portfolio/new/', PortfolioCreateView.as_view(), name="portfolio_new"),
	path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name ="portfolio_detail"),
	path('success/', Success.as_view(), name ="success"),
	path('', PortfolioListView.as_view(), name = 'home'),
]