from rest_framework.test import APITestCase
from rest_framework import status
from .models import CV
from .serializers import CVSerializer

class CVAPITestCase(APITestCase):
    def setUp(self):
        self.users = []
        for i in range(1, 7):
            user = CV.objects.create(
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
            self.users.append(user)
        self.cv = self.users[4]

    def test_cv_list(self):
        url = "/api/cv/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lastnames = [u['lastname'] for u in response.data]
        for i in range(1, 7):
            self.assertIn(f"User-{i}", lastnames)
        self.assertTrue(any(u['contacts']['email'] == f"user3@example.com" for u in response.data))

    def test_cv_retrieve(self):
        url = f"/api/cv/{self.cv.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], "Test")
        self.assertEqual(response.data["lastname"], "User-5")
        self.assertEqual(response.data["contacts"]["phone"], "+1234567805")

    def test_cv_create(self):
        url = "/api/cv/"
        data = {
            "firstname": "Test",
            "lastname": "User-7",
            "skills": "Python, Django",
            "projects": "Project 7",
            "bio": "Passionate Fullstack developer 7.",
            "contacts": {
                "email": "user7@example.com",
                "phone": "+1234567807"
            }
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contacts"]["email"], "user7@example.com")
        self.assertEqual(response.data["lastname"], "User-7")

    def test_cv_update(self):
        url = f"/api/cv/{self.cv.id}/"
        updated_data = {
            "firstname": "Test",
            "lastname": "User-5",
            "skills": "Python, Django, REST",
            "projects": "Updated Project",
            "bio": "Updated bio!",
            "contacts": {
                "email": "user5updated@example.com",
                "phone": "+380991234567"
            }
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated bio!")
        self.assertEqual(response.data["contacts"]["email"], "user5updated@example.com")

    def test_cv_delete(self):
        url = f"/api/cv/{self.cv.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CV.objects.filter(id=self.cv.id).exists())

    def test_serializer_valid(self):
        valid = {
            "firstname": "Test",
            "lastname": "User-8",
            "skills": "Python, Django",
            "projects": "Project 8",
            "bio": "Passionate Fullstack developer 8.",
            "contacts": {
                "email": "user8@example.com",
                "phone": "+1234567808"
            }
        }
        ser = CVSerializer(data=valid)
        self.assertTrue(ser.is_valid(), ser.errors)

    def test_serializer_invalid_email(self):
        data = {
            "firstname": "Test",
            "lastname": "User-BadEmail",
            "skills": "Python",
            "projects": "Something",
            "bio": "Something",
            "contacts": {
                "email": "bademail",
                "phone": "+1234567890"
            }
        }
        ser = CVSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertIn("contacts", ser.errors)

    def test_serializer_invalid_phone(self):
        data = {
            "firstname": "Test",
            "lastname": "User-BadPhone",
            "skills": "Python",
            "projects": "Something",
            "bio": "Something",
            "contacts": {
                "email": "user@example.com",
                "phone": "12345"
            }
        }
        ser = CVSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertIn("contacts", ser.errors)

    def test_serializer_missing_email(self):
        data = {
            "firstname": "Test",
            "lastname": "User-MissingEmail",
            "skills": "Python",
            "projects": "Something",
            "bio": "Something",
            "contacts": {
                "phone": "+1234567890"
            }
        }
        ser = CVSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertIn("contacts", ser.errors)

    def test_serializer_accepts_extra_fields(self):
        data = {
            "firstname": "Test",
            "lastname": "User-Extras",
            "skills": "Python",
            "projects": "Something",
            "bio": "Something",
            "contacts": {
                "email": "extras@example.com",
                "phone": "+1234567890",
                "telegram": "@extras",
                "linkedin": "test-link"
            }
        }
        ser = CVSerializer(data=data)
        self.assertTrue(ser.is_valid(), ser.errors)
