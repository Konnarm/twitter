from django.test import SimpleTestCase


class HomePageTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_home_page_contains_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, 'id="root"')
