import os
import unittest
import datetime

# Configure your app to use the testing configuration
os.environ["CONFIG_PATH"] = "synonyms.config.TestingConfig"

import synonyms
from synonyms.filters import *
  
class FilterTests(unittest.TestCase):
    def testDateFormat(self):
        # Tonight we're gonna party...
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    def testDateFormatNone(self):
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)  

if __name__ == "__main__":
    unittest.main()