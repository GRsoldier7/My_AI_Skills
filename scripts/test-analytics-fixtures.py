"""Execute the portable retention SQL against synthetic data using SQLite."""
from pathlib import Path
import sqlite3
import unittest

ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / 'skills/engineering/data-analytics-engine/references/cohort-retention.sql'


class RetentionFixtures(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.executescript('''
            CREATE TABLE user_cohort(user_id INTEGER, cohort_month INTEGER);
            CREATE TABLE activity_months(user_id INTEGER, activity_month INTEGER);
            CREATE TABLE reporting_months(month_index INTEGER, is_complete INTEGER);
        ''')
        self.db.executemany('INSERT INTO user_cohort VALUES (?, ?)', [(i, 0) for i in range(1, 11)])
        self.db.executemany('INSERT INTO reporting_months VALUES (?, ?)', [(1, 1), (2, 1), (3, 0), (13, 1)])
        self.db.executemany('INSERT INTO activity_months VALUES (?, ?)', [(1, 1), (1, 1), (2, 1), (1, 13)])

    def rows(self):
        return {row[1]: row for row in self.db.execute(SQL.read_text())}

    def test_two_of_ten_is_twenty_percent_despite_duplicate_activity(self):
        row = self.rows()[1]
        self.assertEqual(row[2:5], (2, 10, 0.2))

    def test_complete_month_without_activity_is_zero(self):
        self.assertEqual(self.rows()[2][4], 0)

    def test_incomplete_month_without_activity_is_unknown(self):
        self.assertIsNone(self.rows()[3][4])

    def test_month_offset_does_not_wrap_after_twelve_months(self):
        self.assertEqual(self.rows()[13][4], 0.1)

    def test_unknown_customer_does_not_inflate_numerator(self):
        self.db.execute('INSERT INTO activity_months VALUES (99, 1)')
        self.assertEqual(self.rows()[1][4], 0.2)

    def test_duplicate_cohort_records_do_not_inflate_denominator(self):
        self.db.execute('INSERT INTO user_cohort VALUES (1, 0)')
        self.assertEqual(self.rows()[1][2:5], (2, 10, 0.2))

    def test_separate_cohorts_remain_separate(self):
        self.db.execute('INSERT INTO user_cohort VALUES (20, 1)')
        rows = list(self.db.execute(SQL.read_text()))
        next_cohort = [r for r in rows if r[0] == 1 and r[1] == 0][0]
        self.assertEqual(next_cohort[3:5], (1, 0))


if __name__ == '__main__':
    unittest.main()
