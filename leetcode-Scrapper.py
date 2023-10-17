#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium')


# In[2]:


pip install webdriver-manager


# In[3]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import pandas as pd
import time


# In[4]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# In[5]:


driver.get('')


# In[6]:


from selenium.webdriver.common.keys import Keys

# webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


# In[10]:


webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


# In[11]:





# In[6]:


# driver.find_elements(By.XPATH, '/html/body/app-root')[0].click()


# In[ ]:





# In[2]:


class Solution:
    def __init__(self):
        self.problem = []
        self.companies = []
        self.tags = []
    
    def wait(self,seconds):
        time.sleep(seconds)
    
    def get_problem(self,index):
        problem_name = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[1]/a')
#         print(problem_name[0].text)
        return problem_name[0].text


    def open_cmp_dialog(self,index):
        company_box = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[4]')
        company_box[0].click()

    def get_company_names(self):
        company_list = driver.find_elements(By.XPATH, '/html/body/app-root/app-problem-list/div[2]/div/div/div[2]/div')
        companies_name = company_list[0].text
        res_list = re.findall('[A-Z][^A-Z]*', companies_name)
        # print(res_list)
        return res_list

    def open_tags_box(self,index):
        tag_box = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[5]/button/span[1]')
        tag_box[0].click()

    def close_cmp_diag(self):
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    def next_page(self):
        next_page = driver.find_element(By.CLASS_NAME, 'pagination-next')
        next_page.click()

    def get_tag_names(self):
        company_list = driver.find_elements(By.XPATH, '/html/body/app-root/app-problem-list/div[2]/div/div/div[2]/div')
        companies_name = company_list[0].text
        res_list = re.findall('[A-Z][^A-Z]*', companies_name)
        # print(res_list)
        return res_list

    def dfs(self):
        """
        for each page we will call this function
        """
        problem = []
        companies = []
        tags = []
        for index in range(1, 11):
            #------------------------------------------------------
            problem.append(self.get_problem(index))
            # print("done getting problem \n")
            #------------------------------------------------------


            #------------------------------------------------------
            self.wait(5)
            try:
                company_box = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[4]')
                company_box[0].click()
            # print("done opening company box")
            except:
                self.close_cmp_diag()
                self.open_cmp_dialog(index)
            # print("done opening company box \n")
            #------------------------------------------------------    


            #------------------------------------------------------    
            self.wait(8)
            companies.append(self.get_company_names())
            #  print("done getting company names")
            #------------------------------------------------------


            #------------------------------------------------------
            self.wait(8)
            self.close_cmp_diag()
            #  print("closing the company dialoge")
            #------------------------------------------------------


            #------------------------------------------------------
            self.wait(4)
            try:
                tag_box = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[5]/button/span[1]')
                tag_box[0].click()
            #  print("done opening tag box")
            except:
                self.close_cmp_diag()
                self.open_tags_box(index)
            #  print("done opening tag box \n")
            self.wait(5)
            tags.append(self.get_tag_names())
            self.close_cmp_diag()
#             print("-------------------------------------------------------\n\n")
            #------------------------------------------------------

        return problem, companies, tags


    def call_page_by_page(self,page_no):
        self.wait(8)
#         print(f"----------getting data for {page_no} page-------------")

        probs, coms, tag = self.dfs()
        self.problem.extend(probs)
        self.companies.extend(coms)
        self.tags.extend(tag)
        self.wait(8)

        # after every 5 pages save the data
        if page_no % 5 == 0:
            template = {
            "problems" : self.problem,
            "companies" : self.companies,
            "tags" : self.tags
            }

            df = pd.DataFrame(template)
            df.to_csv(f"F:/questions_{page_no}.csv")
            
            # we make our lists storage empty
            self.problem = []
            self.companies = []
            self.tags = []

        self.wait(4)
        self.next_page()
        
        self.wait(3)
        self.call_page_by_page(page_no+1)


sol = Solution()
sol.call_page_by_page(121)


# In[ ]:





# In[19]:





# In[12]:


for index in range(1,11):
    difficulty = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[6]/span')
    print(difficulty[0].text)


# In[1]:


class Solution:
    def __init__(self):
        self.diff = []
     
    
    def wait(self,seconds):
        time.sleep(seconds)
    

    def next_page(self):
        next_page = driver.find_element(By.CLASS_NAME, 'pagination-next')
        next_page.click()

    
    def get_difficulties(self,index):
        difficulty = driver.find_elements(By.XPATH, f'/html/body/app-root/app-problem-list/div[1]/table/tbody/tr[{index}]/td[6]/span')
        return difficulty[0].text
    
    def dfs(self):
        """
        for each page we will call this function
        """
        difficulty = []
        
        for index in range(1, 11):
            difficulty.append(self.get_difficulties(index))

        return difficulty


    def call_page_by_page(self,page_no):
        self.wait(2)
#         print(f"----------getting data for {page_no} page-------------")

        p = self.dfs()
        self.diff.extend(p)
        
        self.wait(2)

        # after every 5 pages save the data
        if page_no % 20 == 0:
            template = {
            "problems" : self.diff,
            
            }

            df = pd.DataFrame(template)
            df.to_csv(f"F:/difficulty_{page_no}.csv")
            
            # we make our lists storage empty
            self.diff = []
            self.wait(2)
            

        
        self.next_page()
        
        self.wait(2)
        self.call_page_by_page(page_no+1)


sol = Solution()
sol.call_page_by_page(1)


# In[ ]:





# In[ ]:




