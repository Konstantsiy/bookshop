from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.BookView.as_view(), name='main'),
    path('about/', views.about, name='about'),
    path('search/', views.Search.as_view(), name='search'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('registration/', views.RegisterFormView.as_view(), name='registration'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('filter/<slug:slug>/', views.filter_by_genre, name='filter'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add_to_cart/<slug:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('delete_from_cart/<slug:slug>/', views.DeleteFromCartView.as_view(), name='delete_from_cart'),
]
