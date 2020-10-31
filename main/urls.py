from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BookView.as_view(), name='main'),
    path('about/', views.about, name='about'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
]
