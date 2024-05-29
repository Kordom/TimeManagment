from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer'),
    path('search/', views.search, name='search'),
    path('register/', views.register_user, name='register-url'),
]