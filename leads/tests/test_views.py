from django.test import TestCase
from django.shortcuts import reverse
# Create your tests 
class LandingPageTest(TestCase):
    
    def test_status_code(self):
        #if the function starts with test if will automatically
        #run the test
        response = self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing.html")
        