"""
Util class
"""
from datetime import datetime
import settings


def parse_timesamp(date, date_format=settings.TIMESTAMP_FORMAT):
    """
    Simple parametric date parser.
    :param date: A date.
    :param date_format: The format.
    :return: Python date object.
    """
    return datetime.strptime(date, date_format)


def parse_action(value, min_action=1, max_action=5):
    """
    Parse game actions.
    :param value: Action number.
    :param min_action: Min range.
    :param max_action: Max range.
    :return: The value.
    """
    action = int(value)
    if value < min_action or value > max_action:
        raise ValueError('Action out of range')
    return action


def cassandra_insert(session, uid, action, timestamp):
    """
    Inserts data into Cassandra table.
    :param session: Cassandra session object.
    :param uid: User id.
    :param action: Action number.
    :param timestamp: Timestamp.
    :return: None.
    """
    session.execute(
        """
        INSERT INTO actions (uid, action, timestamp)
        VALUES (%s, %s, %s);
        """,
        (uid, action, timestamp.strftime(settings.TIMESTAMP_FORMAT))
    )
