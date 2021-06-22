# -*- coding: utf-8 -*-

import unittest
from stocks.collector import Collector


class CollectorTestCase(unittest.TestCase):
    """ This class represents collector test case """

    def setUp(self) -> None:
        """Define test variables and initialize app."""
        # self.app = create_app(config_name="testing")
        # self.client = self.app.test_client
        pass

    @staticmethod
    def test_collector_execute() -> None:
        collector = Collector()
        collector.execute()


if __name__ == "__main__":
    unittest.main()
