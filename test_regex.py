import re
import unittest
from regex_service import PATTERN

class TestDateRegex(unittest.TestCase):
    pattern = re.compile(PATTERN)


    def test_valid_dates(self):
        valid_dates = [
            "01.01.2024",  
            "31.12.1999",  
            "29.02.2020",  
            "28.02.2021",  
            "15.08.1947",  
            "01.01.2000",  
        ]
        for date in valid_dates:
            with self.subTest(date=date):
                self.assertIsNotNone(self.pattern.fullmatch(date))

    def test_invalid_dates(self):
        invalid_dates = [
            "31-12-1999",  
            "31.12.99",    
            "abcd.ef.ghij",
        ]
        for date in invalid_dates:
            with self.subTest(date=date):
                self.assertIsNone(self.pattern.fullmatch(date))

    def test_search_valid_dates(self):
        strings = [
            "Сегодня 01.01.2024, а завтра 02.01.2024.",
            "Даты: 31.12.1999, 15.08.1947.",
        ]
        expected_matches = [
            ["01.01.2024", "02.01.2024"],
            ["31.12.1999", "15.08.1947"],
        ]
        for string, expected in zip(strings, expected_matches):
            with self.subTest(string=string):
                self.assertEqual(self.pattern.findall(string), expected)

    def test_substitution(self):
        string = "События: 01.01.2024 и 31.12.1999."
        expected_result = "События: [DATE] и [DATE]."
        result = self.pattern.sub("[DATE]", string)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
