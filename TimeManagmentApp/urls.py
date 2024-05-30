from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project'),
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='customer'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('search/', views.search, name='search'),
    path('register/', views.register_user, name='register-url'),
    path('cabinet/', views.my_cabinet, name='profile'),

]