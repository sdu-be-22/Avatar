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
  
  
 	path('update_item/', views.updateItem, name="update_item"),
  	path('process_order/', views.processOrder, name="process_order"),
]