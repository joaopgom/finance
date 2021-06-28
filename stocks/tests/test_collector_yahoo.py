# -*- coding: utf-8 -*-

import time
import unittest
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.keys import Keys
from stocks.collector import YahooCollector


class YahooCollectorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.collector = YahooCollector()

    def test_remove_default_filter(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        eua_filter = self.collector.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]")
        class_filter_eua = 'Bgc($hoverBgColor) Mend(5px) D(ib) Bdrs(3px) filterItem Mb(3px)'
        self.assertIsNot(eua_filter.get_attribute('class'), class_filter_eua)

    def test_open_country_filter_tab(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        class_filter_country = 'D(ib) Mb(3px) filterAdd'
        self.assertEqual(add_filter_country.get_attribute('class'), class_filter_country)
        add_filter_country.click()

    def test_find_add_country_filter(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        class_add_filter_country = 'D(ib) Mb(3px) filterAdd'
        self.assertEqual(add_filter_country.get_attribute('class'), class_add_filter_country)

    def test_find_input_country_filter(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.collector.find_input_country_filter(add_filter_country)
        class_input_filter_country = 'Bd(0) H(28px) Bgc($lv3BgColor) C($primaryColor) W(100%) Fz(s) Pstart(28px)'
        self.assertEqual(input_filter_country.get_attribute('class'), class_input_filter_country)

    def test_find_check_country_filter(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.collector.find_input_country_filter(add_filter_country)
        input_filter_country.send_keys(self.collector.region)
        checkbox_filter_country = self.collector.find_check_filter_country(add_filter_country)
        class_check_filter_country = 'Ta(c) Pos(r) Va(tb) Pend(10px)'  # 'Fl(start) D(b) Mb(10px)'
        self.assertEqual(checkbox_filter_country.get_attribute('class'), class_check_filter_country)

    def test_filter_added(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.collector.find_input_country_filter(add_filter_country)
        input_filter_country.send_keys(self.collector.region)
        checkbox_filter_country = self.collector.find_check_filter_country(add_filter_country)
        checkbox_filter_country.click()
        added_filter = self.collector.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li/button/span")
        self.assertEqual(added_filter.text, self.collector.region)

    def test_find_button_stocks(self) -> None:
        self.collector.open_site()
        button_find_stocks = self.collector.find_button_find_stocks()
        class_button_find_stocks = 'Bgc($linkColor) C(white) Fw(500) Px(20px) Py(9px) Bdrs(3px) Bd(0) Fz(s) D(ib) ' \
                                   'Whs(nw) Miw(110px) Op(0.3)'
        self.assertEqual(button_find_stocks.get_attribute('class'), class_button_find_stocks)

    def test_find_stocks_table(self) -> None:
        self.collector.open_site()
        self.collector.remove_default_filter()
        add_filter_country = self.collector.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.collector.find_input_country_filter(add_filter_country)
        input_filter_country.send_keys(self.collector.region)
        checkbox_filter_country = self.collector.find_check_filter_country(add_filter_country)
        checkbox_filter_country.click()

        button_find_stocks = self.collector.find_button_find_stocks()
        button_find_stocks.click()
        # click not working, so use Keys.RETURN
        button_find_stocks.send_keys(Keys.RETURN)

        # TODO: change this, implement something that waits for the results to load
        time.sleep(5)
        stocks_table_body = self.collector.find_stocks_table()
        self.assertIsInstance(stocks_table_body, FirefoxWebElement)

    def test_collect_stocks(self):
        self.collector.open_site()
        self.collector.remove_default_filter()
        self.collector.add_country_filter()
        self.collector.search_stocks()
        stocks = self.collector.collect_stocks()
        self.assertIsInstance(stocks, dict)
        for stock_symbol in stocks:
            stock = stocks[stock_symbol]
            self.assertTrue(stock_field in stock for stock_field in ['symbol', 'name', 'price'])

    def tearDown(self) -> None:
        self.collector.driver.close()
        self.collector.driver.quit()


