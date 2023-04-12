from datetime import datetime
from hashlib import md5
from ics import (
    Calendar,
    DisplayAlarm,   
    Event,
)
import re
from urllib import parse


BASE_URLS = {
    'google': 'https://calendar.google.com/calendar/render',
    'outlook': 'https://outlook.office.com/owa/',
    'yahoo': 'http://calendar.yahoo.com'
}

INPUT_DATE_FORMAT = "%Y%m%dT%H%M%S"
OUTLOOK_DATE_FORMAT = '%Y-%m-%dT%I:%M:%SZ'
TRIGGER_DATE_FORMAT = '%Y-%m-%dT%I:%M'


def _build_url(baseurl, args_dict):
    url_parts = list(parse.urlparse(baseurl))
    url_parts[4] = parse.urlencode(args_dict)
    return parse.urlunparse(url_parts)


class Add2Cal():

    def __init__(
        self,
        title,
        start,
        end,
        description,
        location,
        timezone
    ):
        self.start_datetime = start
        self.end_datetime = end
        self.event_title = title
        self.event_location = location
        self.timezone = timezone
        self.event_description = description
        self.trigger_datetime = datetime.strptime(
            start, INPUT_DATE_FORMAT).strftime(TRIGGER_DATE_FORMAT)
        self.event_uid = self._get_uid([
            start,
            end,
            self.event_title,
            self.event_location,
            self.event_description,
            self.timezone])

    def _get_uid(self, params):
        param_hash = md5(str(params).encode('utf-8'))
        return param_hash.hexdigest()

    def google_calendar_url(self):
        dates = "%s/%s" % (
            self.start_datetime,
            self.end_datetime)
        params = {
            'action': 'TEMPLATE',
            'text': self.event_title,
            'dates': dates,
            'details': self.event_description,
            'location': self.event_location,
            'pli': 1,
            'uid': self.event_uid,
            'sf': 'true',
            'ctz': self.timezone,
            'output': 'xml',
            'followup': 'https://calendar.google.com/calendar/',
            'scc': 1,
            'authuser': 0
        }
        return _build_url(BASE_URLS['google'], params)

    def yahoo_calendar_url(self):
        end = datetime.strptime(self.end_datetime, INPUT_DATE_FORMAT)
        start = datetime.strptime(self.start_datetime, INPUT_DATE_FORMAT)

        duration_datetime = end - start
        duration_seconds = duration_datetime.seconds
        duration_days = duration_datetime.days
        duration_hours, remainder = divmod(duration_seconds, 3600)
        duration_minutes, seconds = divmod(remainder, 60)
        if duration_days > 0:
            duration_hours += duration_days * 24
        params = {
            'v': 60,
            'view': 'd',
            'type': 20,
            'uid': '',
            'title': self.event_title,
            'st': self.start_datetime,
            'in_loc': self.event_location,
            'dur': '{:02d}{:02d}'.format(duration_hours, duration_minutes),
            'desc': self.event_description
        }
        return _build_url(BASE_URLS['yahoo'], params)

    def outlook_calendar_url(self):
        end = datetime.strptime(self.end_datetime, INPUT_DATE_FORMAT)
        start = datetime.strptime(self.start_datetime, INPUT_DATE_FORMAT)

        params = {
            'path': '/calendar/action/compose',
            'startdt': start.strftime(OUTLOOK_DATE_FORMAT),
            'enddt': end.strftime(OUTLOOK_DATE_FORMAT),
            'subject': self.event_title,
            'uid': self.event_uid,
            'location': self.event_location,
            'body': self.event_description,
            'allday': ''
        }
        return _build_url(BASE_URLS['outlook'], params)

    def ical_content(self):
        c = Calendar()
        e = Event()
        e.alarms = [DisplayAlarm(trigger=self.trigger_datetime)]
        e.name = self.event_title
        e.description = self.event_description
        e.location = self.event_location
        e.begin = self.start_datetime
        e.end = self.end_datetime
        c.events.add(e)
        ics_str = str(c)
        ics_str = re.sub(r'DTSTAMP\:(\d+)T(\d+)Z', r'DTSTAMP:\1T\2', ics_str)
        ics_str = re.sub(r'DTEND\:(\d+)T(\d+)Z',
                         r'DTEND;TZID=%s:\1T\2' % self.timezone, ics_str)
        ics_str = re.sub(r'DTSTART\:(\d+)T(\d+)Z',
                         r'DTSTART;TZID=%s:\1T\2' % self.timezone, ics_str)
        return ics_str

    def as_dict(self, *args, **kwargs):
        return {
            'outlook_link': '',
            'gcal_link': self.google_calendar_url(),
            'yahoo_link': self.yahoo_calendar_url(),
            'ical_content': self.ical_content()
        }
