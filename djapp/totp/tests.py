from django.test import (
    TestCase,
    Client,
)

# Create your tests here.

from . import views

client = Client()

class TotpTest(TestCase):

    def test_totop(self):

        res = client.get("/totp/")

        self.assertContains(res, "Hello")

