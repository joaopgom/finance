# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .entities import StockEntity
from selenium.common.exceptions import NoSuchElementException


class YahooCollector:
    """ Collect Stocks info from Yahoo Finance """
    URL = 'https://finance.yahoo.com/screener/new'

    def __init__(self, region: str = 'Argentina'):
        self.region = region
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(webdriver.FirefoxProfile(), options=options)

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
        return add_filter_country.find_element_by_xpath(path_input_country_filter)

    @staticmethod
    def find_check_filter_country(add_filter_country) -> FirefoxWebElement:
        path_checkbox_country_filter = 'div[1]/div[1]/div[1]/div[1]/div[2]/ul/li/label'
        return add_filter_country.find_element_by_xpath(path_checkbox_country_filter)

    def add_country_filter(self):
        add_filter_country = self.find_add_country_filter()
        add_filter_country.click()
        input_filter_country = self.find_input_country_filter(add_filter_country)
        input_filter_country.send_keys(self.region)
        checkbox_filter_country = self.find_check_filter_country(add_filter_country)
        checkbox_filter_country.click()

    def find_button_find_stocks(self):
        path_button_find_stocks = "//div[@id='screener-criteria']/div[2]/div[1]/div[3]/button[1]"
        return self.driver.find_element_by_xpath(path_button_find_stocks)

    def search_stocks(self):
        button_find_stocks = self.find_button_find_stocks()
        button_find_stocks.click()
        # click not working, so use Keys.RETURN
        button_find_stocks.send_keys(Keys.RETURN)

    def find_stocks_table(self):
        # TODO: change this, implement something that waits for the results to load
        time.sleep(5)
        path_table_body = "//div[@id='Lead-5-ScreenerResults-Proxy']/section/div/div[2]/div/table/tbody"
        return self.driver.find_element_by_xpath(path_table_body)

    @staticmethod
    def stocks_to_stocks_entity(table_rows: list) -> list:
        # TODO: finish this method
        stocks_list = []
        for tr in table_rows:
            cels = tr.find_elements(By.TAG_NAME, 'td')
            stocks = StockEntity()
            for index, cel in enumerate(cels):
                if index == 0:
                    cel_link = cel.find_element(By.TAG_NAME, 'a')
                    stocks.symbol = cel_link.text
                elif index == 1:
                    stocks.name = cel_link.text
                elif index == 2:
                    cel_span = cel.find_element(By.TAG_NAME, 'span')
                    stocks.price = cel_span.text
                else:
                    break
            stocks_list.append(stocks)
        return stocks_list  # {stocks_item.symbol: stocks_item.as_dict() for stocks_item in stocks_list}

    def collect_stocks(self) -> dict:
        stocks_table = self.find_stocks_table()
        table_rows = stocks_table.find_elements(By.TAG_NAME, 'tr')
        stocks_list = self.stocks_to_stocks_entity(table_rows)
        return {stocks_item.symbol: stocks_item.as_dict() for stocks_item in stocks_list}

    def execute(self) -> None:
        try:
            self.open_site()
            self.remove_default_filter()
            self.add_country_filter()
            self.search_stocks()
            stocks = self.collect_stocks()
        except NoSuchElementException:
            pass
        finally:
            self.driver.close()
            self.driver.quit()
            return stocks or {}


STRATEGY_COLLECTOR = {
    'default': YahooCollector
}


class Collector:
    """ Default class to run a collector strategy """
    def __init__(self, strategy: str = None, region: str = None):
        self.strategy = strategy or 'default'
        self.region = region

    def execute(self) -> None:
        strategy = STRATEGY_COLLECTOR[self.strategy](self.region)
        return strategy.execute()
