import unittest
import flask
import json
import sched.models
from datetime import datetime, timedelta

class ModelsTest(unittest.TestCase):

    def test_duration(self):
        now = datetime.now()
        appointment = sched.models.Appointment(
            title='Important Meeting',
            start=now,
            end=now + timedelta(seconds=1800),
            allday=False,
            location='The Office')
        self.assertEqual(1800, appointment.duration)

    def test_title(self):
        now = datetime.now()
        appointment = sched.models.Appointment(
            title='Important Meeting',
            start=now,
            end=now + timedelta(seconds=1800),
            allday=False,
            location='The Office')
        self.assertEqual('Important Meeting', appointment.title)

    def test_location(self):
        now = datetime.now()
        appointment = sched.models.Appointment(
            title='Important Meeting',
            start=now,
            end=now + timedelta(seconds=1800),
            allday=False,
            location='The Office')
        self.assertEqual('The Office', appointment.location)

    def test_representation(self):
        now = datetime.now()
        appointment = sched.models.Appointment(
            id=1,
            title='Important Meeting',
            start=now,
            end=now,
            allday=False,
            location='The Office')
        self.assertEqual('<Appointment: 1>', appointment.__repr__())

if __name__ == '__main__':
    unittest.main()
