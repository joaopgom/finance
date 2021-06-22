# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class YahooCollector:
    """ Collect Stocks info from Yahoo Finance """
    URL = 'https://finance.yahoo.com/screener/new'

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.URL)

    def remove_default_filter(self) -> None:
        """ By default the site open with EUA filter """
        eua_filter = self.driver.find_element_by_xpath(
            "//div[@id='screener-criteria']/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]")
        eua_filter.click()

    def execute(self) -> None:
        self.remove_default_filter()


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
