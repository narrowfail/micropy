"""
Data structures created to solve the task.
"""
import numpy as np


class DynamicActionArray(object):
    """
    Dynamic to store user ids, actions and timestamps using a NumPy structured
    array.
    """

    def __init__(self, size, grow_factor, score_values):
        self.dtype = [('uid', np.int32), ('action', np.int8),
                      ('timestamp', 'datetime64[us]')]
        self.length = 0
        self.size = size
        self.grow_factor = grow_factor
        self.score_values = np.array(score_values)
        self._npa = np.zeros(self.size, dtype=self.dtype)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        return self._npa[index]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self._npa[:self.length])

    def append(self, uid, action, timestamp):
        """
        Append a new record to the array.
        :param uid: User ID.
        :param action: Action performed by the user.
        :param timestamp: Action date and time.
        :return: None.
        """
        # Resie like a Java ArrayList
        if self.length == self.size:
            self.size = int(self.grow_factor * self.size)
            self._npa = np.resize(self._npa, self.size)
        # Add item
        self._npa[self.length] = (uid, action, timestamp)
        self.length += 1

    def query(self, uid, start, end):
        """
        Given user ID and start and end timestamps, return how many events of
        each type there are and how many points this player has scored.
        :param uid: User ID.
        :param start: Start timestamp.
        :param end: End timestamp.
        :return: List of tuples per action (occurrences, score).
        """

        # Condition
        condition = ((self._npa['uid'] == uid) &
                     (self._npa['timestamp'] >= start) &
                     (self._npa['timestamp'] <= end))
        # Count actions
        count = np.bincount(
            np.extract(condition, self._npa[:self.length])['action'],
            minlength=len(self.score_values) + 1)[1:]

        # Multiply actions by score
        score = np.multiply(count, self.score_values)

        return zip(count, score)
