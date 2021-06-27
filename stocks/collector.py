# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webelement import FirefoxWebElement
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class YahooCollector:
    """ Collect Stocks info from Yahoo Finance """
    URL = 'https://finance.yahoo.com/screener/new'

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        # caps = DesiredCapabilities.FIREFOX
        # caps['marionette'] = False
        self.driver = webdriver.Firefox(webdriver.FirefoxProfile(), options=options)  # (options=options)

    def open_site(self):
        self.driver.get(self.URL)

    def remove_default_filter(self) -> None:
        """ By default the site open with EUA filter """
        eua_filter = self.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]")
        eua_filter.click()

    def find_add_country_filter(self) -> FirefoxWebElement:
        country_filter_button = self.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[last()]")
        return country_filter_button

    @staticmethod
    def find_input_country_filter(add_filter_country) -> FirefoxWebElement:
        path_input_country_filter = '//div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input'
        input_filter_country = add_filter_country.find_element_by_xpath(path_input_country_filter)
        return input_filter_country

    @staticmethod
    def find_check_filter_country(add_filter_country) -> FirefoxWebElement:
        path_checkbox_country_filter = 'div[1]/div[1]/div[1]/div[1]/div[2]/ul/li/label'
        checkbox_filter_country = add_filter_country.find_element_by_xpath(path_checkbox_country_filter)
        return checkbox_filter_country

    def add_country_filter(self):
        add_filter_country = self.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.find_input_country_filter(add_filter_country)
        input_filter_country.send_keys('Argentina')
        checkbox_filter_country = self.find_check_filter_country(add_filter_country)
        checkbox_filter_country.click()
        self.check_filter_country()

    def find_button_find_stocks(self):
        path_button_find_stocks = "//div[@id='screener-criteria']/div[2]/div[1]/div[3]/button[1]"
        button_find_stocks = self.driver.find_element_by_xpath(path_button_find_stocks)
        return button_find_stocks

    def search_stocks(self):
        button_find_stocks = self.find_button_find_stocks()
        button_find_stocks.click()

    def execute(self) -> None:
        self.open_site()
        self.remove_default_filter()
        self.add_country_filter()
        self.search_stocks()
        #self.collect_stocks()


STRATEGY_COLLECTOR = {
    'default': YahooCollector
}


class Collector:
    """ Default class to run a collector strategy """
    def __init__(self, strategy: str = None):
        self.strategy = strategy or 'default'

    def execute(self) -> None:
        strategy = STRATEGY_COLLECTOR[self.strategy]()
        strategy.execute()
