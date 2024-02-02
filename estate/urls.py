from django.urls import path
from . import views


urlpatterns = [
    path('', views.estate, name='estate'),
    path('for_sale/', views.for_sale, name='for_sale'),
    path('for_rent/', views.for_rent, name='for_rent'),
    path('submit_property/', views.submit_property, name='submit_property'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register_request, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout_request, name='logout'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('search_and_filter', views.search_and_filter, name='search_and_filter')
]
