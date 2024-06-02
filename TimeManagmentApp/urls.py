from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>', views.ProjectDetailView.as_view(), name='project'),
    path('projects/<int:pk>/assign_workers/', views.assign_workers_to_project, name='assign-workers'),
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='customer'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('workers/', views.WorkerListView.as_view(), name='workers'),
    path('workers/<int:pk>', views.WorkerDetailView.as_view(), name='worker'),
    path('createtask/', views.UserTaskCreateView.as_view(), name='add-task'),
    path('createproject/', views.UserProjectCreateView.as_view(), name='add-project'),
    path('createworker/', views.UserWorkerCreateView.as_view(), name='add-worker'),
    path('createvehicle/', views.UserVehicleCreateView.as_view(), name='add-vehicle'),
    path('assigngroups/', views.UserWorkerGroupCreateView.as_view(), name='assign-groups'),


    path('search/', views.search, name='search'),
    path('register/', views.register_user, name='register-url'),
    path('mycabinet/', views.my_cabinet, name='profile'),

]