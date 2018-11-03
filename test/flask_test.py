import unittest
from  app import app



class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_view(self):
        tester=app.test_client(self)
        response = tester.get('/add', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_analyse_view(self):
        response = self.tester.get('/analyse', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_compares_view(self):
        response = self.tester.get('/compare', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_route(self):
        response = self.tester.get('/add', content_type='html/text')
        self.assertTrue(b'Enter Twitter Handle' in response.data)

    def test_analyse_route(self):
        response = self.tester.get('/analyse', content_type='html/text')
        self.assertTrue(b'Enter Twitter Username' in response.data)

    def test_index_route(self):
        response = self.tester.get('/index', content_type='html/text')
        self.assertTrue(b'Personality Score' in response.data)

    def test_compare_route(self):
        response = self.tester.get('/compare', content_type='html/text')
        self.assertTrue(b'Personality Rec' in response.data)

    def test_index_view(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)