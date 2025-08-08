from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    
    path('book_list', views.book_list, name='book_list'),
    path('book_overviews', views.book_overviews, name='book_overviews'),
    path('book_profile', views.book_profile, name='profile'),
    path('create/', views.book_create, name='book_create'),
#    path('update/', views.book_update, name='book_update'),
    path('update/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
]
