from django.urls import path
from . import views
from .views import log

urlpatterns = [
    path('',log.as_view()),
    path('home', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('login', log.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/update/', views.service_update, name='service_update'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('services/subscribe/', views.subscription_create, name='subscription_create'),
    path('subscription/callback/', views.subscription_callback, name='subscription_callback'),
]
