import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_success(self):
        self.assertEqual(extract_title("# this is a title\nno title here"), "this is a title")

    def test_no_title(self):
        self.assertRaises(ValueError, extract_title, "## too many number signs")


if __name__ == "__main__":
    unittest.main()
