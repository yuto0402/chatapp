from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class Test(TestCase):

    def setUp(self):
        self.response = self.client.get