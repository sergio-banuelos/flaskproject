import unittest
import flask
import json
import sched.app
from datetime import datetime, timedelta

class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = sched.app.app.test_client()
    
    def test_appointments_redirect_login(self):
        response = self.app.get("/appointments/")
        self.assertEquals(response.status_code, 302)
        assert 'Important Meeting' not in response.data

    def test_create_appointments_redirect_login(self):
        response = self.app.get("/appointments/create/")
        self.assertEquals(response.status_code, 302)
        assert 'Important Meeting' not in response.data
    
    def test_login(self):
        response = self.app.get("/login/")
        self.assertEquals(response.status_code, 200)
        response2 = self.app.post("/login/",
        data = dict(
                username = 'admin@cimat.mx',
                password = 'admin',
                ), follow_redirects = True)
        self.assertEquals(response2.status_code, 200)
        assert 'Important Meeting' in response2.data

    def test_create_and_edit(self):
        response = self.app.get("/login/")
        self.assertEquals(response.status_code, 200)
        response2 = self.app.post("/login/",
        data = dict(
            username = 'admin@cimat.mx',
            password = 'admin',
            ), follow_redirects = True)
        self.assertEquals(response2.status_code, 200)
        response = self.app.get("/appointments/create/")
        self.assertEquals(response.status_code, 200)
        assert 'Add' in response.data
        assert 'Edit' not in response.data
        response2 = self.app.post("/appointments/create/",
        data=dict(
            title='Pruebas',
            start='2014-11-07 06:00:00',
            end='2014-11-08 15:00:00',
            location='Home',
            description='Insertado en el num. 2',
        ), follow_redirects=True)
        self.assertEquals(response2.status_code, 200)
        assert 'Pruebas' in response2.data
        response = self.app.get("/appointments/2/edit/")
        self.assertEquals(response.status_code, 200)
        assert 'Edit Appointment' in response.data
        response2 = self.app.post("/appointments/2/edit/",
        data=dict(
            title='Pruebas',
            start='2014-11-07 07:00:00',
            end='2014-11-08 16:00:00',
            location='Work',
            description='Editado en el num. 2',
            ), follow_redirects=True)
        self.assertEquals(response2.status_code, 200)
        assert 'Work' in response2.data
    
    def test_delete(self):
        response = self.app.get("/login/")
        self.assertEquals(response.status_code, 200)
        response2 = self.app.post("/login/",
        data = dict(
            username = 'admin@cimat.mx',
            password = 'admin',
            ), follow_redirects = True)
        self.assertEquals(response2.status_code, 200)
        response = self.app.delete(
            "/appointments/2/delete/", follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'status': 'OK'})


if __name__ == '__main__':
    unittest.main()
