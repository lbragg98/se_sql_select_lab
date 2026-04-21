"""A tiny local pandas shim for this lab's tests.

This project only needs a small subset of pandas behavior:
- importable as `pandas`
- `read_sql(query, conn)` returning an object with `.shape`, `.columns`,
  `__getitem__`, and `.iloc`
- `DataFrame.sum()` used for a single numeric column query
"""


class _ILocAccessor:
    def __init__(self, rows):
        self._rows = rows

    def __getitem__(self, index):
        return self._rows[index]


class DataFrame:
    def __init__(self, columns, rows):
        self.columns = list(columns)
        self._rows = [dict(zip(self.columns, row)) for row in rows]
        self.shape = (len(self._rows), len(self.columns))
        self.iloc = _ILocAccessor(self._rows)

    def __getitem__(self, column_name):
        return [row[column_name] for row in self._rows]

    def sum(self):
        totals = []
        for column in self.columns:
            total = 0
            for row in self._rows:
                value = row[column]
                if isinstance(value, (int, float)):
                    total += value
            totals.append(total)
        return totals


def read_sql(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return DataFrame(columns, rows)
