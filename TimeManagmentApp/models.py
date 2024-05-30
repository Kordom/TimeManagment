from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Project(models.Model):
    name = models.CharField('Project name', max_length=50)
    description = models.TextField('Project desription')
    place_city = models.CharField('City', max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, verbose_name='Customer', null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.place_city} {self.description[:30]}'


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    role = models.CharField('Role', max_length=255)
    price_per_hour = models.FloatField('Price per hour', default=0)
    skills = models.TextField('Skills')

    AVAILABILITY_STATUS = (
        ('ISA', 'Available'),
        ('ONV', 'On vacation'),
        ('ONS', 'On working site'),
        ('OFF', 'On the way home'),
        ('ONW', 'On the way to work'),
        ('NOT', 'Not Available')
    )

    status = models.CharField(
        max_length=3,
        choices=AVAILABILITY_STATUS,
        default='NOT',
        help_text='Worker availability status'
    )

    def __str__(self):
        return f"{self.user.username} {self.role} {self.price_per_hour} {self.status}"


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=6, unique=True)
    car_model = models.CharField('Car model', max_length=50)
    car_make = models.CharField('Car make', max_length=50)
    capacity = models.IntegerField('Capacity (1-8)', validators=[MaxValueValidator(8), MinValueValidator(1)])

    def __str__(self):
        return f'{self.car_make} {self.car_model} {self.license_plate} {self.capacity}'


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

    def __str__(self):
        return f"{self.title} Priority: {self.priority}"


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

    def __str__(self):
        return f"{self.customer_name} {self.customer_number}"


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

