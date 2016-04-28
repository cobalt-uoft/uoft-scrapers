from datetime import datetime


def get_current_month():
    """Return current month."""
    now = datetime.now()
    return '%s-%s' % (now.year, now.month)


def get_campus_id(d, campus):
    """Return campus id, made up of date and specifier (one of SG, M, SC)."""
    d = datetime.strptime(d, '%Y-%m-%d')
    return '%s%s' % (str(d.day).zfill(2), campus)


def is_date_in_month(d, m):
    """Determine if the given date is in the given month."""
    d, m = datetime.strptime(d, '%Y-%m-%d'), datetime.strptime(m, '%Y-%m')
    return d.month == m.month


def convert_time(dt):
    """Convert datetime from ISO 8601 format to seconds since midnight."""
    dt = datetime.strptime(dt[:19], '%Y-%m-%dT%H:%M:%S')
    return dt.hour * 60 * 60 + dt.minute * 60
