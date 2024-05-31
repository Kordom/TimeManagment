from django.contrib import admin
from .models import *


# Register your models here.

class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask
    extra = 0


class WorkerTaskInline(admin.TabularInline):
    model = WorkerTask
    extra = 0


class WorkerGroupTaskInline(admin.TabularInline):
    model = WorkerGroup
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project_start','project_end', 'customer')
    inlines = (ProjectTaskInline, WorkerGroupTaskInline,)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'price_per_hour', 'skills', 'status', 'availability_date')
    list_editable = ('availability_date','status')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'due_date', 'status')
    list_editable = ('status', 'priority', 'due_date',)
    inlines = (ProjectTaskInline, WorkerTaskInline)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'car_model', 'car_make', 'capacity')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_number', 'customer_main_office')


@admin.register(WorkerGroup)
class WorkerGroupAdmin(admin.ModelAdmin):
    list_display = ('project', 'vehicle', 'worker')
    list_filter = ('vehicle__license_plate',)


@admin.register(WorkerTask)
class WorkerTaskAdmin(admin.ModelAdmin):
    list_display = ('worker', 'task')


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'task')
    list_filter = ('project__place_city', 'task__priority')


admin.site.register(Comment)
admin.site.register(Profile)

