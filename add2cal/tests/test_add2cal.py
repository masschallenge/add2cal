import unittest
import arrow
from add2cal import Add2Cal
from datetime import datetime
from urllib import parse
from pytz import timezone

DATE_FORMAT = "%Y%m%dT%H%M%S"

EXPECTED_CONTENT = "BEGIN:VCALENDAR"
DESCRIPTION_CONTENT = 'DESCRIPTION:this is an exciting event'
LOCATION_CONTENT = 'LOCATION:narnia'


class TestAdd2Cal(unittest.TestCase):
    def setUp(self):
        start = datetime.now().strftime(
            DATE_FORMAT)
        end = start
        title = 'test event'
        description = 'this is an exciting event'
        location = 'narnia'
        self.timezone = 'America/New_York'
        self.add2cal = Add2Cal(
            start=start,
            end=end,
            title=title,
            description=description,
            location=location,
            timezone=self.timezone)

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

    def test_ical_content(self):
        self.maxDiff = None
        self.add2cal.start_datetime = arrow.get(datetime.now())
        self.add2cal.end_datetime = arrow.get(datetime.now())
        tz = timezone(self.timezone)
        start = datetime.now().astimezone(tz).strftime(DATE_FORMAT)
        self.add2cal.trigger_datetime = datetime.strptime(start, DATE_FORMAT)
        content = self.add2cal.ical_content()
        self.assertIn(
            EXPECTED_CONTENT,
            content
        )

    def test_ical_content_contains_description_and_location(self):
        self.maxDiff = None
        self.add2cal.start_datetime = arrow.get(datetime.now())
        self.add2cal.end_datetime = arrow.get(datetime.now())
        tz = timezone(self.timezone)
        start = datetime.now().astimezone(tz).strftime(DATE_FORMAT)
        self.add2cal.trigger_datetime = datetime.strptime(start, DATE_FORMAT)
        content = self.add2cal.ical_content()
        for elem in [LOCATION_CONTENT, DESCRIPTION_CONTENT]:
            self.assertIn(elem, content)

