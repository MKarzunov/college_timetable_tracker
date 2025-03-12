import unittest
from main import check_announcements, get_announcements
import bs4

class CheckerTest(unittest.TestCase):
    def setUp(self):
        self.normal_announcements = get_announcements()
        self.minus_one_announcements = self.normal_announcements[1:]
        self.minus_two_announcements = self.normal_announcements[2:]
        self.no_announcements = ['0', '0', '0']
    def test_login_error(self):
        self.assertEqual(check_announcements(None, [None]),
                         ('LoginError', []))
    def test_no_updates(self):
        self.assertEqual(check_announcements(self.normal_announcements, self.normal_announcements),
                         ('NoUpdates', []))
    def test_no_equality_found(self):
        self.assertEqual(check_announcements(self.normal_announcements, self.no_announcements),
                         ('NoEqualityFound', self.normal_announcements))
    def test_equality_found_one(self):
        self.assertEqual(check_announcements(self.normal_announcements, self.minus_one_announcements),
                         ('EqualityFound', self.normal_announcements[:1]))
    def test_equality_found_two(self):
        self.assertEqual(check_announcements(self.normal_announcements, self.minus_two_announcements),
                         ('EqualityFound', self.normal_announcements[:2]))

if __name__ == '__main__':
    unittest.main()