import scrapy
from scrapy.http import FormRequest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By 
from ..items import DemoItem
import time

class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["finance.vietstock.vn"]
    # start_urls = ["https://pagination.js.org"]

    def start_requests(self):
        urls=[
            'https://finance.vietstock.vn/doanh-nghiep-a-z'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'url':url})
    
    def extract_page_data(driver):
        page_output=[]
        page_elements=driver.find_element(By.XPATH,'//*[@id="demo1"]/div[2]/div/ul/li[9]/a').click()


    def parse(self, response, url):
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.get(url)
        driver.maximize_window()
        login_button=driver.find_element(By.XPATH,'/html/body/div[2]/div[6]/div[1]/div[1]/div/a[2]').click()
        time.sleep(2)
        user_textbox=driver.find_element(By.XPATH,'//*[@id="txtEmailLogin"]')
        pass_textbox=driver.find_element(By.XPATH,'//*[@id="txtPassword"]')
        user_textbox.send_keys('tcnam20009@gmail.com')
        time.sleep(2)
        pass_textbox.send_keys('nam20009')
        time.sleep(2)
        login_button2=driver.find_element(By.XPATH,'//*[@id="btnLoginAccount"]/i').click()
        time.sleep(5)
        number_of_pages = int(driver.find_element(By.XPATH,'//*[@id="az-container"]/div[1]/div[2]/div/span[1]/span[2]').text)
        item=DemoItem()
        item['number_of_pages']=number_of_pages
        for _ in range (number_of_pages):
            next_page=driver.find_element(By.XPATH,'//*[@id="btn-page-next"]/i').click()
            time.sleep(5)
        yield item

        driver.quit()
        
