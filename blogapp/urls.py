from venv import create
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('create',views.create, name='create'),
    path('readmore/<int:val>',views.readmore, name='readmore'),
    path('profile/<str:val>',views.profile, name='profile'),
    path('profile/edit/<int:val>',views.edit, name='edit'),
    path('profile/delete/<int:val>',views.delete, name='delete'),
    path('search',views.search, name='search'),
    path('category/<str:val>',views.category, name='category'),
    path('cmt', views.cmt, name='cmt'),
    path('about',views.about,name='about'),
    ]