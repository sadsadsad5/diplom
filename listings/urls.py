from django.urls import path
from . import views
from listings.views import statistics_view
urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('create/', views.create_listing, name='create_listing'),
    path('my-listings/', views.user_listings, name='user_listing'),
    path('update/<int:pk>/', views.update_listing, name='update_listing'),
    path('delete/<int:pk>/', views.delete_listing, name='delete_listing'),
    path('statistics/', statistics_view, name='statistics'),
]
