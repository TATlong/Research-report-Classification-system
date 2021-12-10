#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 22:59:25 2018
@author: lilong
"""

import re
import os
import time
import time
import lxml
import traceback
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ReportReptile:

    def __init__(self):
        self.filedir = "reptile_files"
        self.phantomjs_path = "./phantomjs-2.1.1-macosx/bin/phantomjs"
        self.url = "http://data.eastmoney.com/report/hgyj.html"   # 原始页面
        self.driverInit()   # 初始化driver

    def driverInit(self):
        """浏览器驱动初始化"""

        service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']
        self.driver = webdriver.PhantomJS(executable_path=self.phantomjs_path,
                                          # service_args=service_args     # 这里加了反而报错
                                          )

        # 获取初始页面，因为页面的网址不变，只需第一次获取即可
        self.driver.get(self.url)

    def get_page_num(self, num):
        """模拟鼠标点击下一页"""

        # （1）定位到表格下面页码选择区域，定位元素："macresearch_table_pager"
        element_page = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "macresearch_table_pager")))

        # （2）获取搜索页面的按钮"ipt"
        tr_options = element_page.find_element_by_class_name("ipt")

        # （3）填入页码，模拟点击鼠标
        tr_options.clear()  # 必须清空当前的搜索页码
        tr_options.send_keys('{}'.format(str(num)))
        element_page.find_element_by_class_name("btn").click()

        # （4）点击后必须等待固定时长
        time.sleep(10)

    def download_report(self, text_link, re_sum_info):
        """根据送入的url和标签，然后保存到本地"""
        text_tmp = "\n".join([str(s) for s in re_sum_info])

        # 获取页面内容
        orihtml = requests.get(text_link).content
        soup = BeautifulSoup(orihtml, "lxml")

        # 判断报告是否是空页
        if soup.find('div', class_='ctx-content') == None:
            return None

        page_con = []
        for a in soup.find('div', class_='ctx-content').find_all('p'):
            page_con.append(str(a.text))

        file_path = os.path.join(self.filedir, '{}.txt'.format(str(re_sum_info[0])+str(re_sum_info[-1])))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_tmp+"\n".join(page_con))

    def clickUPData(self):
        """模拟按钮，按日期升序排列，主要是根据网页的具体形式调整
        """
        print("开始模拟日期排序 ...")
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "macresearch_table")))

        # 第一次模拟点击
        data_options = element.find_elements_by_tag_name("thead")[0]
        data_options_1 = data_options.find_elements_by_xpath('//*[@id="macresearch_table"]/table/thead/tr/th[6]/a')[0]
        print(f"检查到：{data_options_1.text}")
        data_options_1.click()
        time.sleep(10)

        # 第二次模拟点击
        data_options = element.find_elements_by_tag_name("thead")[0]
        data_options_2 = data_options.find_elements_by_xpath('//*[@id="macresearch_table"]/table/thead/tr/th[6]/a')[0]
        data_options_2.click()
        time.sleep(10)

    def getPageTest(self):
        element_table = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "macresearch_table")))

        # 获取所有的tr标签，"tr"
        tr_options = element_table.find_elements_by_tag_name("tr")

        # 再遍历td标签
        for tr_option in tr_options:
            # 获得：序号、报告名称、作者、机构名称、近一月机构宏观研报数量、日期
            td_options = tr_option.find_elements_by_tag_name("td")  # 定位元素"td"
            re_sum_info = []
            for td_option in td_options:
                re_sum_info.append(td_option.text)
            print("page:", re_sum_info)

    def get_report_page(self, page_start, page_end):
        """ 以起始和终止页面数为爬取标准
        两个参数分别是要爬取的页面：起始页面，终止页面
        """
        print("chrome webdriver start ...")
        for i in range(page_start, page_end + 1):
            try:
                print(f"-----------获取指定页: {i}---------")

                # 每次指定页码
                self.get_page_num(i)
                element_table = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "macresearch_table")))

                # 获取所有的tr标签，"tr"
                tr_options = element_table.find_elements_by_tag_name("tr")

                # 再遍历td标签
                for tr_option in tr_options:
                    # 获得：序号、报告名称、作者、机构名称、近一月机构宏观研报数量、日期
                    td_options = tr_option.find_elements_by_tag_name("td")  # 定位元素"td"
                    re_sum_info = []
                    for td_option in td_options:
                        re_sum_info.append(td_option.text)
                    print("page:", re_sum_info)

                    # 爬取研报正文
                    for i in range(len(td_options)):
                        if i == 1:
                            url_element = td_options[i]
                            if not url_element:
                                continue
                            # print('report title:', td_options[i].text)
                            link = url_element.find_elements_by_xpath(".//*[@href]")[0]  # 获取链接
                            text_link = link.get_attribute('href')
                            self.download_report(text_link, re_sum_info)
                            break

            except Exception as e:
                info = traceback.format_exc()
                print(info)

        # 关闭driver
        self.driver.quit()

    def get_report_date(self, start_date, end_date):
        """ 以起始和终止时期为爬取标准 """

        # 转化为可比较大小的日期
        start_date = time.strptime(start_date, "%Y-%m-%d")
        end_date = time.strptime(end_date, "%Y-%m-%d")

        # 首先对页面进行升序排序，即从最早的开始爬取
        self.clickUPData()

        # # 对页面测试用
        # self.getPageTest()

        # 每次指定页码
        pageNum_init = 1
        FLAG = True
        while FLAG:
            self.get_page_num(pageNum_init)
            print(f"page: {pageNum_init}")
            try:
                element_table = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "macresearch_table")))
                tr_options = element_table.find_elements_by_tag_name("tr")  # 获取所有的tr标签，"tr"

                # 再遍历td标签
                for tr_option in tr_options:
                    # 获得：序号、报告名称、作者、机构名称、近一月机构宏观研报数量、日期
                    td_options = tr_option.find_elements_by_tag_name("td")  # 定位元素"td"
                    re_sum_info = []
                    for td_option in td_options:
                        re_sum_info.append(td_option.text)
                    print("page:", re_sum_info)
                    if not re_sum_info:
                        continue

                    # 日期判断
                    time_tmp = time.strptime(re_sum_info[-1], "%Y-%m-%d")
                    if time_tmp < start_date:
                        continue
                    elif time_tmp > end_date:
                        FLAG = False
                        break
                    else:
                        for i in range(len(td_options)):
                            if i == 1:
                                url_element = td_options[i]
                                if not url_element:
                                    continue
                                # print('report title:', td_options[i].text)
                                link = url_element.find_elements_by_xpath(".//*[@href]")[0]  # 获取链接
                                text_link = link.get_attribute('href')
                                self.download_report(text_link, re_sum_info)
                                break

            except Exception as e:
                info = traceback.format_exc()
                print(info)
                pageNum_init += 1
            pageNum_init += 1

        self.driver.quit()


def main():
    report_obj = ReportReptile()

    # （1）按指定页码
    report_obj.get_report_page(1, 2)

    # （2）按指定日期
    # report_obj.get_report_date('2019-12-10', '2019-12-11')


if __name__ == '__main__':
    main()

    # # 测试
    # phantomjs_path = "./phantomjs-2.1.1-macosx/bin/phantomjs"
    # driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    # driver.get('https://www.baidu.com/')
    # print(driver.title)
    # driver.quit()
