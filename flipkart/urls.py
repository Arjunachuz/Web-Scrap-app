from django.urls import path
from . import views

urlpatterns = [
    path('scrap/',views.scrape_product, name='scrape_product'),
    path('data/<int:pk>/',views.scraped_data, name='scraped_data'),
    path('',views.list_products, name='list_products'),
]