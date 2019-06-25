import unittest
from add2cal import Add2Cal
from datetime import datetime
from urllib import parse

DATE_FORMAT = "%Y%m%dT%H%M%S"


class TestAdd2Cal(unittest.TestCase):
    def setUp(self):
        start = datetime.now().strftime(
            DATE_FORMAT)
        end = start
        title = 'test event'
        description = 'this is an exciting event'
        location = 'narnia'
        self.add2cal = Add2Cal(
            start=start,
            end=end,
            title=title,
            description=description,
            location=location)

    def test_outlook(self):
        outlook_url = self.add2cal.outlook_calendar_url()
        self.assertEqual(
            parse.urlparse(outlook_url).netloc,
            'outlook.office.com'
        )

    def test_google_calendar(self):
        outlook_url = self.add2cal.google_calendar_url()
        self.assertEqual(
            parse.urlparse(outlook_url).netloc,
            'calendar.google.com'
        )

    def test_yahoo_calendar(self):
        outlook_url = self.add2cal.yahoo_calendar_url()
        self.assertEqual(
            parse.urlparse(outlook_url).netloc,
            'calendar.yahoo.com'
        )
