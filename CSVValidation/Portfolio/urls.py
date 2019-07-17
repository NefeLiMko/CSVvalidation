from django.urls import path
from .views import PortfolioListView,PortfolioCreateView,PortfolioDetailView,Success,PortfolioUpdateView,PortfolioDeleteView

app_name = 'port'

urlpatterns = [
	path('portfolio/new/', PortfolioCreateView.as_view(), name="portfolio_new"),
	path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name ="portfolio_detail"),
	path('portfolio/<int:pk>/delete', PortfolioDeleteView.as_view(), name ="portfolio_delete"),
	path('portfolio/<int:pk>/edit', PortfolioUpdateView.as_view(), name ="portfolio_edit"),
	path('success/', Success.as_view(), name ="success"),
	path('', PortfolioListView.as_view(), name = 'home'),
]