from datetime import datetime


def convert_time(t):
    t = [int(x) for x in t.split(':')]

    converted = 0
    for i in range(min(len(t), 3)):
        converted += t[i] * (60 ** (2-i))
    return converted


def get_period(d):
    def get_date(month, date, year):
        month = 'jun' if month == 'june' else month
        return datetime.strptime('%s%s%d' % (year, month, date), '%Y%b%d')

    d = datetime.strptime(d, '%Y-%m-%d')
    year, month = d.year, None

    for m, ld in (('dec', 31), ('apr', 30), ('june', 30), ('aug', 31)):
        if get_date(m, 1, year) <= d <= get_date(m, ld, year):
            month = m
            break

    if month:
        return '%s%s' % (month.upper(), str(year)[2:])


def get_course_id(course_code, date):
        d = datetime.strptime(date, '%Y-%m-%d')

        month, year = d.strftime('%b').lower(), d.year
        month = 'june' if month == 'jun' else month

        endings = {
            'dec': {
                'F': '%d9' % year,
                'Y': '%d9' % (year - 1)
            },
            'apr': {
                'S': '%d1' % year,
                'Y': '%d9' % (year - 1)
            },
            'june': {
                'F': '%d5F' % year,
                'Y': '%d5' % year
            },
            'aug': {
                'S': '%d5S' % year,
                'Y': '%d5' % year
            }
        }

        season = course_code[-1]
        period = get_period(date)

        exam_id = course_id = None

        if month in endings and season in endings[month]:
            course_id = '%s%s' % (course_code, endings[month][season])
            exam_id = '%s%s' % (course_id, period)

        return exam_id, course_id
