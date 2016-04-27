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
