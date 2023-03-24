import re
from selenium import webdriver
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import datetime
# import exceptions
import numpy as np
import requests
import random
import pandas as pd
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium_stealth import stealth
import pickle

# 浏览器配置对象
options = webdriver.ChromeOptions()
# 禁用自动化栏
options.add_experimental_option('excludeSwitches',['enable-automation'])
# 屏蔽保存密码提示框
prefs = {'credentials_enable_service':False,'profile.password_manager_enabled':False}
options.add_experimental_option('prefs',prefs)
# 反爬虫特征处理
options.add_argument('--disable-blink-features=AutomationControlled')

#driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver = webdriver.Chrome(executable_path='D:\\pachong\\chromedriver_win32\\chromedriver.exe',options=options)
driver.implicitly_wait(5)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# 1. 爬取内容

# intialize our Panda's dataframe with the data we want from each item
allItemsPD = pd.DataFrame(data=None, index=None,
                          columns=['title', 'Author', 'Translator','score', 'Reviewer', 'ReviewTime','Review_content','website'
                                   ]);
def get_next(allItemsPD):

    # 1.获取基础信息
    basic_info = driver.find_element_by_css_selector('.overflow-x-hidden').get_attribute('data-amplitude-params')
    # 将basic info 转为字典
    basic_info = eval(basic_info)
    # title
    title = basic_info['novelName']
    Author = basic_info['novelWriter']
    Translator = basic_info['novelTranslator']
    score_info = driver.find_element_by_css_selector('.MuiGrid-root .flex .items-center').text
    # 转换为浮点型,结果保留为了1位小数
    score = round(float(score_info[:2])/20, 1)
    website = "wuxia"
    #点击view all 展开评论
    time.sleep(4)
    driver.find_element_by_css_selector('.inline-block').click()
    time.sleep(2)
    # 获取评论总页数
    # /html/body/div[5]/div[3]/div/div/div/div[2]/div[3]/nav/ul
    pages_info = driver.find_elements_by_css_selector('.MuiPagination-ul .MuiButtonBase-root')
    # /html/body/div[5]/div[3]/div/div/div/div[2]/div[3]/nav/ul/li[9]/button
    next_button = pages_info[-1]
    page_num = 1
    while True:
        # 2 抓取评论
        time.sleep(1)
        # driver.find_element_by_css_selector('rax-textinput rax-textinput-placeholder-6 searchbar-input').send_keys("iphone14")
        divs = driver.find_elements_by_css_selector('.loading-container .rounded-12')
        for div in divs:
            # 二次提取
            Reviewer = div.find_element_by_css_selector('.p-16 .font-set-b14').text
            ReviewTime = div.find_element_by_css_selector('.p-16 .font-set-r12').text

            # 获取评论全部内容
            # 点击show more 展开全部评论
            div.find_element_by_css_selector('.block').click()
            time.sleep(2)
            ReviewContent = div.find_element_by_css_selector('.absolute.font-set-r15-h150')
            span_list = ReviewContent.find_elements_by_tag_name(name='span')

            # 获取评论内容
            Review_content = []
            time.sleep(2)
            for span in span_list:
                span_text = span.get_attribute("innerHTML")
                if span_text[:6] == '<span>':
                    continue
                else:
                    Review_content.append(span_text)
    #/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/article[1]/div/div[2]/div[2]/div[1]
    #/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/article[1]/div/div[2]/div[2]/div[1]/span[2]/span/text()
    #/html/body/div[2]/div[3]/div/div/div/div[2]/div[2]/article[1]/div/div[2]/div[2]/div[1]/span[3]/span/text()
            str = ''
            span_content = str.join(Review_content)
            #print(title, Author, Translator, score, Reviewer,ReviewTime,Review_content,website)

            # 数据保存为字典
            currentItemDict = {'title': title, 'Author': Author, 'Translator': Translator,
                               'score': score, 'Reviewer': Reviewer, 'ReviewTime': ReviewTime,'Review_content':Review_content,'website':website}
            allItemsPD = allItemsPD.append(currentItemDict, ignore_index=True)

        if next_button.is_enabled():
            print("current page:",page_num)
            page_num+=1
            next_button.click()

        else:
            break

    return allItemsPD


driver.get(
        f'https://www.wuxiaworld.com/novels/?genre=Xianxia')
time.sleep(2)
books = driver.find_elements_by_css_selector('.infinite-scroll-component__outerdiv .MuiTypography-root')
links = []
for book in books:
    #
    link = book.find_element_by_tag_name("a").get_attribute('href')
    print("书籍链接",link)
    links.append(link)
# 设置断点index，以防爬取过程中断，中断后，从断点网页继续爬取即可
continue_index=0
for i in range(len(links)-continue_index):
    if i<continue_index:
        i=i+continue_index
    link = links[i]
    time.sleep(2)
    driver.get(link)
    time.sleep(2)
    allItemsPD = get_next(allItemsPD)
    print(f"当前为第{i}个网页，网址为：{link}")
    allItemsPD.to_pickle(f'wuxia_{i}.pkl')
    allItemsPD.to_csv(f"wuxia_{i}.csv",encoding='utf_8_sig')
print("done")

allItemsPD.to_pickle('wuxia.pkl')
allItemsPD.to_csv("wuxia.csv",encoding='utf_8_sig')
