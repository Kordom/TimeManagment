from django.test import TestCase

# Create your tests here.
class Vehicle():
    def __init__(self, capacity):
        self.capacity = capacity


    def is_full(self, n):
        if self.capacity < n:
            print('hi')



v = Vehicle(5)

v.is_full(6)