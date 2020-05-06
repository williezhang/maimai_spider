# -*- coding: utf-8 -*-
import time
import math

import random

from selenium import webdriver#导入库
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import json

import warnings
warnings.filterwarnings('ignore')



def login(geturl,username,password):
    '''
    输入账号、密码模拟登录
    '''
    options=webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_experimental_option('useAutomationExtension',False)  
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(geturl)
    time.sleep(5)
    
#    browser.find_elements_by_class_name("loginPhoneInput")[0].send_keys(username)
    browser.find_elements_by_xpath('//*[@id="form"]/div[1]/div/input')[0].send_keys(username)
    time.sleep(2)
#    browser.find_element_by_id("login_pw").send_keys(password)
    browser.find_elements_by_xpath('//*[@id="login_pw"]')[0].send_keys(password)
    time.sleep(2)
    browser.find_elements_by_xpath('//*[@id="form"]/input[3]')[0].click()
#    browser.find_elements_by_class_name("loginBtn")[0].click()
    print('---------log in-------------')
    return browser




def change_private_open(string):
    string=string[:36]+'.'+string[36:-43]+'.'+string[-43:]
    return string


def search(browser,text,max_condidate):
    '''
    开始搜索
    '''
    max_page=math.ceil(max_condidate/10)
    condidate=[]
    for page in range(max_page):
        search_url='https://maimai.cn/search/contacts?count=10&page={}&query={}&dist=0&searchTokens=&highlight=true&jsononly=1&pc=1'.format(page,text)
        #print(search_url)
        try:
            browser.get(search_url)#get即跳转
            search_html=browser.page_source
            #print(cur_html)
            soup = BeautifulSoup(search_html,'lxml')
            cc = soup.select('pre')[0]
            res = json.loads(cc.text)
            #print(res)
            sub_condidate=res['data']['contacts']
            condidate.extend(sub_condidate)
        except:
            break
    return condidate


def click_everyone(browser,encode_mmid):
    '''
    返回的搜索结果的详细信息
    '''
    if '.' not in encode_mmid:
        url='https://maimai.cn/contact/detail/{}?fr=&from=webview%23%2Fweb%2Fsearch_center'.format(change_private_open(encode_mmid))
        #print('string: ',change_private_open(string))
    else:
        url='https://maimai.cn/contact/detail/{}?fr=&from=webview%23%2Fweb%2Fsearch_center'.format((encode_mmid))
    #print('url: ',url)
    browser.get(url)
    time.sleep(5)
    try:
        work=browser.find_elements_by_xpath('//*[span="工作经历"]/..//ul/div/div[1]/div[1]/div/div[1]/div/div[1]/div/span')[0].text.split('•')
        company=work[0]
        career=work[1]
    except:
        company=''
        career=''
    try:
        work_time=browser.find_elements_by_xpath('//*[span="工作经历"]/..//ul/div/div[1]/div[1]/div/div[1]/div/div[2]')[0].text
    except:
        work_time='' 
    try:   
        school=browser.find_elements_by_xpath('//*[span="教育经历"]/..//ul/div/div[1]/div[1]/div/div[1]/div/div[1]/div/span')[0].text
    except:
        school=''
    try:
        education=browser.find_elements_by_xpath('//*[span="教育经历"]/..//ul/div/div[1]/div[1]/div/div[1]/div/div[2]')[0].text.split('，')
        school_time=education[0]
        major=education[1]
        educational_background=education[2]
    except:
        school_time=''
        major=''
        educational_background=''
    try:
        hometown=browser.find_elements_by_xpath('//*[span="更多资料"]/..//*[span="家乡"]/../div[1]/span')[0].text
    except:
        hometown=''
        
    return [company,career,work_time,school,school_time,major,educational_background,hometown,url]
    
    
def everybody(browser,text,max_condidate=50):
    condidate=search(browser,text,max_condidate)
    #print(condidate)
    if len(condidate)==0:
        return '无查询结果！'
        #return None
    else: 
        num=len(condidate)
        print('有{}条结果'.format(num))
        ret=[]
        for i in range(num):
        #for i in range(1):
            time.sleep(3)
            #print(i)
            #print('查询基本信息')
            everybody_info=condidate[i]['contact']
            name=everybody_info['name']
            gender=everybody_info['gender']
            if gender==0:
                gender='女'
            elif gender==1:
                gender='男'
            else:
                gender=''
            province=everybody_info['province']
            city=everybody_info['city']
            #company=everybody_info['company']
            #career=everybody_info['career']
            hangye=everybody_info['user_pfmj']['pf_name1']+'|'+everybody_info['user_pfmj']['mj_name1']
            encode_mmid=everybody_info['encode_mmid'] 
            #print(i,[name,gender,province,city,company,career,hangye,encode_mmid])
            #print('查询更多信息')
            base_info=[name,gender,province+city,hangye]
            more_info=click_everyone(browser,encode_mmid)
            base_info.extend(more_info)
            ret.append(base_info)
            #print(ret)
#            df=pd.DataFrame(ret)
#            df.rename(columns={0:'姓名',1:'性别',2:'所在城市',3:'行业',4:'公司',5:'职业',6:'工作时间',7:'学校',
#                               8:'在校时间',9:'专业',10:'学历',11:'家乡',12:'个人主页'},inplace=True)
#            df=df[['姓名','性别','行业','公司','职业','工作时间','学校','在校时间','专业','学历','所在城市','家乡','个人主页']]
#        return df
        return ret
 


     
if __name__=='__main__':
    browser=login('https://acc.maimai.cn/login',账号,密码)
    search_result=everybody(browser,'公司 '+'姓名',max_condidate=1)
    
      
