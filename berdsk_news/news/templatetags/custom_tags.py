from datetime import datetime
from django.utils import timezone
from django import template
import zoneinfo

register = template.Library()


@register.simple_tag()
def current_time(format_string='%H:%M of %d %b %Y'):
   return datetime.now().strftime(format_string)


@register.simple_tag()
def current_hour(tz):
   return datetime.now(zoneinfo.ZoneInfo(tz)).hour


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
