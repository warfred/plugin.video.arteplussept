import time
import datetime
from HTMLParser import HTMLParser

from addon import language
import hof

p = HTMLParser()


def colorize(text, color):
    """
    color: a hex color string (RRGGBB or #RRGGBB) or None
    """
    if not color:
        return text
    if color.startswith('#'):
        color = color[1:]
    return '[COLOR ff' + color + ']' + text + '[/COLOR]'


def format_title_and_subtitle(title, subtitle=None):
    label = u'[B]{title}[/B]'.format(title=p.unescape(title))
    # suffixes
    if subtitle:
        label += u' - {subtitle}'.format(subtitle=p.unescape(subtitle))
    return label


def sanitize_string(str):
    return str.encode('ascii', errors='replace')


def parse_date(datestr):
    # remove timezone info
    datestr = datestr[0:25]
    date = None
    # workaround for datetime.strptime not working (NoneType ???)
    try:
        date = datetime.datetime.strptime(datestr, '%a, %d %b %Y %H:%M:%S')
    except TypeError:
        date = datetime.datetime.fromtimestamp(time.mktime(
            time.strptime(datestr, '%a, %d %b %Y %H:%M:%S')))
    return date


def past_week():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    dates = []
    for i in xrange(0, 8):  # TODO: find better interval
        cdate =  today - (one_day * i)
        dates.append((str(cdate), '{d:%A}, {d:%d}'.format(d=cdate)))
    return dates


def eraseElement(d,k):
    if isinstance(d, dict):
        if k in d:
            d.pop(k)
        else:
            print("Cannot find matching key")
    else:
        print("Not able to delete")
