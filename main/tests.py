from django.test import TestCase
from django.urls import reverse
from .models import CV


class CVViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 7):
            CV.objects.create(
                firstname="Test",
                lastname=f"User-{i}",
                skills=f"Python, Django, FastAPI, ...{i}",
                projects=f"Project {i}",
                bio=f"Passionate Fullstack developer {i}.",
                contacts={
                    "email": f"user{i}@example.com",
                    "phone": f"+12345678{i:02d}"
                }
            )
        cls.cv = CV.objects.get(lastname="User-5")

    def assertUsersInResponse(
            self,
            response,
            users_should_be=None,
            users_should_not_be=None
    ):
        """
        Helper to assert presence or absence of specific users by number (ID).
        """
        users_should_be = users_should_be or []
        users_should_not_be = users_should_not_be or []
        for i in users_should_be:
            self.assertContains(response, f"User-{i}")
            self.assertContains(response, f"user{i}@example.com")
        for i in users_should_not_be:
            self.assertNotContains(response, f"User-{i}")
            self.assertNotContains(response, f"user{i}@example.com")

    def test_cv_list_view_status_code_and_template(self):
        url = reverse('cv_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/cv_list.html")

    def test_cv_list_view_content(self):
        response = self.client.get(reverse('cv_list'))
        self.assertUsersInResponse(response, users_should_be=range(1, 7))

    def test_cv_list_pagination_limit(self):
        # Limit 5, so only users 1-5
        response = self.client.get(reverse('cv_list') + "?limit=5")
        self.assertUsersInResponse(
            response,
            users_should_be=range(1, 6),
            users_should_not_be=[6]
        )

        # Only user 6
        response = self.client.get(reverse('cv_list') + "?limit=5&page=2")
        self.assertUsersInResponse(
            response,
            users_should_be=[6],
            users_should_not_be=range(1, 6)
        )

    def test_cv_list_invalid_limit_and_page(self):
        # Invalid limits fall back to default=10.
        for val in ["-1", "0", "foobar"]:
            response = self.client.get(reverse('cv_list') + f"?limit={val}")
            self.assertUsersInResponse(response, users_should_be=range(1, 7))

        # Invalid page defaults to first
        response = self.client.get(reverse('cv_list') + "?page=abc")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User-1")

        # Out-of-range page shows last page (limit 5, so only User-6)
        response = self.client.get(reverse('cv_list') + "?limit=5&page=100")
        self.assertEqual(response.status_code, 200)
        self.assertUsersInResponse(
            response,
            users_should_be=[6],
            users_should_not_be=range(1, 6)
        )

    def test_cv_detail_view_success(self):
        # Should return all details for cv User-5
        url = reverse('cv_detail', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User-5")
        self.assertContains(response, self.cv.skills)
        self.assertContains(response, self.cv.projects)
        self.assertContains(response, self.cv.bio)
        for value in self.cv.contacts.values():
            self.assertContains(response, value)
        self.assertTemplateUsed(response, "main/cv_detail.html")

    def test_cv_detail_view_404(self):
        url = reverse('cv_detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_cv_list_view_context(self):
        response = self.client.get(reverse('cv_list'))
        self.assertIn('cvs', response.context)
        self.assertIn('limit', response.context)
        self.assertIn('limit_options', response.context)
        self.assertGreaterEqual(len(response.context['cvs'].object_list), 1)
        self.assertEqual(response.context['limit_options'], [5, 10, 20, 50])
