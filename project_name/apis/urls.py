from django.urls import path
from .views import home,post_review, get_analysis

urlpatterns = [
    path('home', home, name='home'), 
    path('reviews/', post_review, name='post_review'),
    path('analysis/', get_analysis, name='get_analysis'),
]