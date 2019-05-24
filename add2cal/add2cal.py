from datetime import datetime
from urllib import parse
from ics import Calendar, Event
from ics import DisplayAlarm
import hashlib
from pytz import timezone

BASE_URLS = {
    'google': 'https://calendar.google.com/calendar/render',
    'outlook': 'https://outlook.live.com/owa/',
    'yahoo': 'http://calendar.yahoo.com'
}
DATE_FORMAT = "%Y%m%dT%H%M%SZ"


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
        tz='America/New_York'
    ):
        localtz = timezone(tz)
        self.start_datetime = localtz.localize(datetime.fromtimestamp(start))
        self.end_datetime = localtz.localize(datetime.fromtimestamp(end))
        self.event_title = title
        self.event_location = location
        self.event_description = description
        self.event_timezone = tz
        self.event_uid = self._get_uid([
            start,
            end,
            self.event_timezone,
            self.event_title,
            self.event_location,
            self.event_description])

    def _get_uid(self, params):
        param_hash = hashlib.md5(str(params).encode('utf-8'))
        return param_hash.hexdigest()

    def google_calendar_url(self):
        dates = "%s/%s" % (
            self.start_datetime.strftime(DATE_FORMAT),
            self.end_datetime.strftime(DATE_FORMAT))
        params = {
            'action': 'TEMPLATE',
            'text': self.event_title,
            'dates': dates,
            'ctz': self.event_timezone,
            'details': self.event_description,
            'location': self.event_location,
            'pli': 1,
            'uid': self.event_uid,
            'sf': 'true',
            'output': 'xml',
            'followup': 'https://calendar.google.com/calendar/',
            'scc': 1,
            'authuser': 0
        }
        return _build_url(BASE_URLS['google'], params)

    def yahoo_calendar_url(self):
        params = {
            'v': 60,
            'view': 'd',
            'type': 20,
            'uid': '',
            'title': self.event_title,
            'st': self.start_datetime.strftime(DATE_FORMAT),
            'in_loc': self.event_location,
            'dur': 200,
            'desc': self.event_description
        }
        return _build_url(BASE_URLS['yahoo'], params)

    def outlook_calendar_url(self):
        params = {
            'path': '/calendar/action/compose',
            'rru': 'addevent',
            'startdt': self.start_datetime.strftime(DATE_FORMAT),
            'enddt': self.end_datetime.strftime(DATE_FORMAT),
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
        e.alarms = [DisplayAlarm(trigger=self.start_datetime)]
        e.name = self.event_title
        e.begin = self.start_datetime
        e.end = self.end_datetime
        c.events.add(e)
        return str(c)

    def as_dict(self, *args, **kwargs):
        return {
            'outlook_link': self.outlook_calendar_url(),
            'gcal_link': self.google_calendar_url(),
            'yahoo_link': self.yahoo_calendar_url(),
            'ical_content': self.ical_content()
        }
