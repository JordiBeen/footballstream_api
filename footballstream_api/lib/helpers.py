import datetime
from random import randint
import magic
from sqlalchemy.sql.functions import concat
from sqlalchemy import or_


def random_with_n_digits(n):
    """Generates a string containing only digits
    :param integer length: the length of the string to be returned.
    """
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def is_image(mime_type=None, file_path=None):
    if file_path:
        mime_type = magic.from_file(file_path, mime=True)
    return True if 'image' in str(mime_type).split("/")[0] else False


def get_prev_month(_date):
    """Returns the 1st of the previous month based on value passed in
    :param datetime.date
    """
    first_day_this_month = _date.replace(day=1)
    last_day_prev_month = first_day_this_month - datetime.timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)
    return first_day_prev_month


def get_next_month(_date):
    """Returns the 1st of the next month based on value passed in
    :param datetime.date
    """
    first_day_this_month = _date.replace(day=1)
    some_day_next_month = first_day_this_month + datetime.timedelta(days=32)
    first_day_next_month = some_day_next_month.replace(day=1)
    return first_day_next_month


# used for search with keyword
def keyword_filter(query, keyword, columns):

    keyword = keyword.replace('  ', ' ')
    clauses = []

    for column in columns:
        clause = concat(column).ilike('%{}%'.format(keyword))
        clauses.append(clause)

    query = query.filter(or_(*clauses))

    return query
