from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project'),
    path('projects/update/<int:pk>/', views.UserProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/assign_workers/', views.UserWorkerGroupCreateView.as_view(), name='assign-workers'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('customers/update/<int:pk>/', views.UserCustomerUpdateView.as_view(), name='customer-update'),
    path('workers/', views.WorkerListView.as_view(), name='workers'),
    path('workers/<int:pk>/', views.WorkerDetailView.as_view(), name='worker'),
    path('workers/update/<int:pk>/', views.UserWorkerUpdateView.as_view(), name='worker-update'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TasksDetailView.as_view(), name='task'),
    path('tasks/delete/<int:pk>/', views.UserTaskDeleteView.as_view(), name='done-task'),
    path('tasks/taskmanager/<int:pk>/', views.UserTaskManager.as_view(), name='taskmanager'),

    path('createtask/', views.UserTaskCreateView.as_view(), name='add-task'),
    path('createproject/', views.UserProjectCreateView.as_view(), name='add-project'),
    path('createworker/', views.UserWorkerCreateView.as_view(), name='add-worker'),
    path('createvehicle/', views.UserVehicleCreateView.as_view(), name='add-vehicle'),
    path('assigngroups/', views.UserWorkerGroupCreateView.as_view(), name='assign-groups'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicles'),
    path('vehicles/<int:pk>', views.VehicleDetailView.as_view(), name='vehicle'),
    path('vehicles/update/<int:pk>', views.UserVehicleUpdateView.as_view(), name='vehicle-update'),



    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('search/', views.search, name='search'),
    path('register/', views.register_user, name='register-url'),
    path('mycabinet/', views.my_cabinet, name='profile'),
    path('workers/<int:pk>/workerdelete', views.UserDeleteView.as_view(), name='worker-delete'),

]