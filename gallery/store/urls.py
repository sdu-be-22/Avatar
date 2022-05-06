from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
 	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
 	path('location/', views.location, name="location"),
	path('collections/', views.collections, name="collections"),
	path('contacts/', views.contacts, name="contacts"),
 	path('about/', views.about, name="about"),
  	path('news/', views.news, name="news"),
  
 	path('update_item/', views.updateItem, name="update_item"),
  	path('process_order/', views.processOrder, name="process_order"),

#uTo-code
	path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
#/uTo-code
]