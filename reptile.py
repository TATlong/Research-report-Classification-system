#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 22:59:25 2018

@author: lilong
"""
from interface import Interface_base

import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Report(object):
    
    def __init__(self,filedir):
        Interface_base.__init__(self)  # 初始化父类
        self.filedir=filedir
        self.driver=webdriver.PhantomJS() # 初始化就启动模拟器
        
    
    # 根据送入的url,模拟鼠标点击页面获得下一页面的url
    def get_page_url(self,url,num):        
        self.driver.get(url)
        element_page = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "PageNav")))       
        tr_options = element_page.find_elements_by_id("gopage") 
        # 模拟点击鼠标，获得该页的url
        tr_options[0].clear() 
        tr_options[0].send_keys('{}'.format(str(num)))  
        element_page.find_element_by_class_name("btn_link").click()
        self.url=self.driver.current_url
        
        
    # 根据送入的url和时期、标题、机构，然后保存到本地
    def download_report(self,text_link,re_sum_info):
        self.report_num=self.report_num+1
        text_tmp=str(re_sum_info)
        orihtml = requests.get(text_link).content        
        soup = BeautifulSoup(orihtml,"lxml" )    
        if soup.find('div',class_='newsContent')==None:  # 判断报告是否是空页
            return None
        for a in soup.find('div',class_='newsContent').find_all('p'):            
            text_tmp=text_tmp+str(a)+'\n'
            
        with open(self.filedir+self.time+'{}.txt'.format(str(self.report_num)),"w",encoding="utf-8") as f:
            f.write(text_tmp)
            
         
         
    # 以起始和终止页面数为爬取标准
    def get_report_page(self,page_start,page_end):             
        try:   
            #driver = webdriver.Chrome()  # 打开模拟器                       
            for i in range(page_start,page_end+1):
                self.driver=webdriver.PhantomJS()   # 防止断开，所以每次遍历重新打开                  
                self.get_page_url(self.url,i)                
                self.driver.get(self.url)
                element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "dt_1")))            
                tr_options = element.find_elements_by_tag_name("tr")
                
                for tr_option in tr_options:
                    td_options = tr_option.find_elements_by_tag_name("td")  
                    re_sum_info=''          
                    for td_option in td_options:  # 获得时间、标题、机构名
                        re_sum_info=re_sum_info+td_option.text+'\n'
                          
                    for td_option in td_options: # 爬取研报正文
                        text_url = td_option.find_elements(By.CLASS_NAME, "report_tit")
                        if len(text_url)==0:
                            continue
                        print('report title:',td_option.text)
                        for link in text_url[0].find_elements_by_xpath(".//*[@href]"):
                            text_link=link.get_attribute('href')
                            self.download_report(text_link,re_sum_info)
                self.driver.quit()  # 遍历一遍后关闭
            
        except Exception as e:
            print (str(e))
                
        finally:
            self.driver.quit()  # 关闭模拟器
           
                       
    # 以起始和终止时期为爬取标准        
    def get_report_date(self,start_date,end_date):  
        start_date=time.strptime(start_date,"%Y-%m-%d")  # 转化为可比较大小的日期
        end_date=time.strptime(end_date,"%Y-%m-%d")        
        self.driver.get(self.url)
        element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "PageCont")) ) 
        page=[]
        Page_options = element.find_elements_by_tag_name("a")
        for pp in Page_options:
            page.append(pp.text)
        print(page[-3])
        page_last=int(page[-3])
        if page_last<100:  # 这里是为了防止页面结构发生变化，抓取到的最后页面的页面数抓取错误
            page_last=200
        else: page_last=page_last
        flag_stop=0   # 退出继续爬取下去的标志
        try:   
            page_tem=1
            while(page_tem<=page_last and flag_stop==0):
                self.driver=webdriver.PhantomJS()
                self.get_page_url(self.url,page_tem)   # 模拟点击鼠标，获得该页的url
                self.driver.get(self.url)
                element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "dt_1")) )            
                tr_options = element.find_elements_by_tag_name("tr")
                
                for tr_option in tr_options:
                    td_options = tr_option.find_elements_by_tag_name("td")  
                    re_sum_info=''
                    info_tem=[]  
                    for td_option in td_options:  # 获得时间、标题、机构名
                        info_tem.append(td_option.text)
                        re_sum_info=re_sum_info+td_option.text+'\n'
                    if len(info_tem)==0: pass
                    else: 
                        tt=time.strptime(info_tem[0],"%Y-%m-%d")
                        if tt>=start_date and tt<=end_date:
                            print('info_tem:',info_tem[0])  
                                                      
                            for td_option in td_options:   # 爬取研报正文
                                text_url = td_option.find_elements(By.CLASS_NAME, "report_tit")
                                if len(text_url)==0:
                                    continue
                                print('report title:',td_option.text)
                                for link in text_url[0].find_elements_by_xpath(".//*[@href]"):
                                    text_link=link.get_attribute('href')
                                    self.download_report(text_link,re_sum_info)
                                    #print('text_link:',text_link)                                                       
                        if tt<start_date: flag_stop=1                   
                page_tem=page_tem+1  
                self.driver.quit()
                
        except Exception as e:
            print (str(e))       
        finally:
            self.driver.quit()  # 关闭模拟器
            
   
        
      
'''
# get_report(1,4)中的两个参数分别是要爬取的页面：起始页面，终止页面                          
def main():
    report_obj=Report("http://data.eastmoney.com/report/hgyj.html")
    #print(report_obj.get_report_page(1,1))
    print(report_obj.get_report_date('2018-11-9','2018-11-12'))

if __name__ == '__main__':
    main()
'''









