from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
import datetime
from django.utils import timezone


class Project(models.Model):
    name = models.CharField('Project name', max_length=50)
    description = models.TextField('Project desription')
    place_city = models.CharField('City', max_length=50, null=True, blank=True)
    project_start = models.DateTimeField()
    project_end = models.DateTimeField()
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, verbose_name='Customer', null=True, blank=True)

    picture = models.ImageField(upload_to='project_pics', blank=True, default='no-image.png')

    def __str__(self):
        return f'{self.name} {self.place_city} {self.description[:30]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    role = models.CharField('Role', max_length=255)
    price_per_hour = models.FloatField('Price per hour', default=0)
    skills = models.TextField('Skills')

    AVAILABILITY_STATUS = (
        ('ISA', 'Available'),
        ('NOT', 'Not Available')
    )

    status = models.CharField(
        max_length=3,
        choices=AVAILABILITY_STATUS,
        default='NOT',
        help_text='Worker availability status'
    )
    availability_date = models.DateField('Available From', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.role} {self.price_per_hour} {self.status}"

    @property
    def total_wage(self):
        """
        Calculate the total wage for the worker based on price per hour.
        """
        total_wage = 0
        for task in self.workertask_set.all():
            total_wage += task.task.duration_hours * self.price_per_hour
        return total_wage


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=6, unique=True)
    car_model = models.CharField('Car model', max_length=50)
    car_make = models.CharField('Car make', max_length=50)
    capacity = models.IntegerField('Capacity (1-8)', validators=[MaxValueValidator(8), MinValueValidator(1)])
    picture = models.ImageField(upload_to='vehicle_pics', blank=True, default='no-image.png')

    def __str__(self):
        return f'{self.car_make} {self.car_model} {self.license_plate} {self.capacity}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)

    @property
    def is_full(self):
        return self.capacity <= self.workergroup_set.count()

    @property
    def num_workers(self):
        return self.workergroup_set.count()

class Task(models.Model):
    title = models.CharField('Task name', max_length=255)
    description = models.TextField("Task description", blank=True, null=True)

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('INPS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='TO_DO',
                              help_text='Task status')
    priority = models.IntegerField('Priority (0-5)', validators=[MaxValueValidator(5), MinValueValidator(0)])
    due_date = models.DateTimeField('Should be done')
    duration_hours = models.IntegerField('Duration (hours)', default=0)

    def __str__(self):
        return f"{self.title} Priority: {self.priority}"

    @property
    def is_overdue(self):
        if self.due_date and timezone.make_aware(datetime.datetime.now()) > self.due_date:
            return True
        else:
            return False


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'


class Customer(models.Model):
    customer_name = models.CharField('Customer name', max_length=50, null=True)
    customer_number = models.CharField('Customer number', max_length=50, null=True)
    customer_main_office = models.CharField('Customer main office', max_length=50, null=True)

    picture = models.ImageField(upload_to='customer_pics', blank=True, default='no-image.png')

    def __str__(self):
        return f"{self.customer_name} {self.customer_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # numatytieji Model klases veiksmai suvykdomi
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)


class WorkerGroup(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} {self.worker} {self.vehicle}"


class WorkerTask(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.worker} {self.task}"


class ProjectTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} {self.task}"


class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', blank=True, default='default-user.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # numatytieji Model klases veiksmai suvykdomi
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)
