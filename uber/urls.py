from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('booking/', views.booking, name='booking'),
    path('payment/<int:ride_id>/',views.payment_view, name='payment'),
    path('receipt/<int:payment_id>/', views.receipt_view, name='receipt'),
]