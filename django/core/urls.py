from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('movie/', views.MovieListView.as_view(), name='MovieList'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='MovieDetail'), 
]