import scrapy
from ..items import EnterpriseItem
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..decorators.myDecorators import ProgressBar, extract_href_from_a_tag
import time

class EnterpriseSpider(scrapy.Spider):
    name = "enterprise"
    allowed_domains = ['finance.vietstock.vn']
    # start_urls = ["https://finance.vietstock.vn"]

    def start_requests(self):
        urls=[
            "https://finance.vietstock.vn/doanh-nghiep-a-z"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'url':url})
    
    def parse(self, response, url):   
        # inspect_response(response,self)
        options=webdriver.EdgeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver=webdriver.Edge(capabilities=desired_capabilities)
        driver.get(url)
        driver.implicitly_wait(5)
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
        for _ in range (number_of_pages):
            table=driver.find_element(By.CSS_SELECTOR,'.table, .table-striped, .table-bordered, .table-hover, .table-middle, .pos-relative, .m-b')
            # table_body=table.find_element(By.TAG_NAME,"tbody")
            rows=table.find_elements(By.XPATH,"//tr") ## find 'tr' tag in whold html 
            for row in rows:
                cols=row.find_elements(By.XPATH,".//td") # find 'td' tag in current sub
                count=0
                item=EnterpriseItem()
                for col in cols:
                    if count==0:
                        item['soTT']=col.text
                    if count==1:
                        item["maCK"]=col.text      
                        item["link"]=extract_href_from_a_tag(col.get_attribute('innerHTML'))
                    elif count==2:
                        item["tenCTY"]=col.text
                    elif count==3:
                        item["nganh"]=col.text
                    elif count==4:
                        item["san"]=col.text
                    elif count==5:
                        item["klGD"]=col.text
                        count=0
                        break
                    count+=1    
                yield item
            next_page=driver.find_element(By.XPATH,'//*[@id="btn-page-next"]/i').click()
            time.sleep(2)
        driver.quit()
        
# <table class="table table-striped table-bordered table-hover table-middle pos-relative m-b">