# -*- coding: utf-8 -*-

import unittest
from stocks.collector import YahooCollector


class YahooCollectorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_remove_default_filter(self) -> None:
        collector = YahooCollector()
        collector.remove_default_filter()
        eua_filter = collector.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]")
        class_filter_eua = 'Bgc($hoverBgColor) Mend(5px) D(ib) Bdrs(3px) filterItem Mb(3px)'
        self.assertIsNot(eua_filter.get_attribute('class'), class_filter_eua)
