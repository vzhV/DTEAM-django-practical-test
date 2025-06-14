from django.test import TestCase, Client
from django.urls import reverse

from audit.constants import SKIP_LOG_PATHS
from audit.models import RequestLog
from main.models import CV


class RequestLogMiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logging_normal_view(self):
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.status_code, 200)
        log = RequestLog.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.method, 'GET')
        self.assertTrue(log.path == '/')
        self.assertEqual(log.query_string, '')
        self.assertIsInstance(log.timestamp, type(log.timestamp))

    def test_logging_with_querystring(self):
        response = self.client.get(reverse('cv_list') + '?limit=5&page=2')
        self.assertEqual(response.status_code, 200)
        log = RequestLog.objects.last()
        self.assertIn('limit=5', log.query_string)
        self.assertIn('page=2', log.query_string)
        self.assertEqual(log.method, 'GET')
        self.assertTrue(log.path == '/' or log.path == reverse('cv_list'))

    def test_logging_detail_view(self):
        cv = CV.objects.create(
            firstname="Test",
            lastname="User",
            skills="Python, Django, FastAPI, ...",
            projects="Project",
            bio="Passionate Fullstack developer.",
            contacts={
                "email": "user@example.com",
                "phone": "+12345678"
            }
        )
        detail_url = reverse('cv_detail', args=[cv.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        log = RequestLog.objects.last()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, detail_url)

    def test_skipped_paths_are_not_logged(self):
        for skip_path in SKIP_LOG_PATHS:
            count_before = RequestLog.objects.count()
            self.client.get(skip_path)
            count_after = RequestLog.objects.count()
            self.assertEqual(count_before, count_after)

    def test_post_request_is_logged(self):
        response = self.client.post(reverse('cv_list'))
        self.assertEqual(response.status_code, 200)
        log = RequestLog.objects.last()
        self.assertEqual(log.method, 'POST')
        self.assertTrue(log.path == '/')

    def test_recent_requests_view(self):
        self.client.get(reverse('cv_list'))
        self.client.get(reverse('cv_list'))
        self.client.get(reverse('cv_list'))
        response = self.client.get('/logs/')
        self.assertEqual(response.status_code, 200)
        logs = RequestLog.objects.order_by('-timestamp')[:10]
        for log in logs:
            self.assertContains(response, log.method)
            self.assertContains(response, log.path)
            self.assertContains(response, log.timestamp.strftime('%Y-%m-%d'))

    def test_remote_ip_logging(self):
        self.client.get(reverse('cv_list'), REMOTE_ADDR="8.8.8.8")
        log = RequestLog.objects.last()
        self.assertEqual(log.remote_ip, "8.8.8.8")
