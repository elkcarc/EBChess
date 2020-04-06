from django.test import TestCase, RequestFactory
from helloworld.views import HomePageView

class HelloWorldTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

