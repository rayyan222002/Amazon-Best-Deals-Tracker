#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install selenium


# In[3]:


pip install bs4


# In[4]:


pip install webdriver_manager


# In[5]:


pip install pandas


# In[79]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# In[80]:


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[81]:


# For serching the desired item

try:
    search_term = 'sd card'
    driver.get("https://www.amazon.in/")
    text_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    text_box.clear()
    text_box.send_keys(search_term)
    text_box.submit()
except:
    driver.implicitly_wait(15)


# In[82]:


from bs4 import BeautifulSoup
import pandas as pd


# In[83]:


page_source = driver.page_source
type(page_source)


# In[84]:


soup = BeautifulSoup(page_source, 'html')
type(soup)


# In[85]:


soup.prettify()


# In[86]:


products = soup.find_all('div', {'data-component-type': 's-search-result'})
len(products)


# In[88]:


url = 'https://www.amazon.in/s?k=sd+card'
dealslist = []
amazon_url = 'https://www.amazon.in'


# In[89]:


def getdata(url):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html')
    return soup


# In[90]:


def getdeals(soup):
    for item in products:
        title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        short_title = title.strip()[:25]
        link_text = item.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
        link = amazon_url+link_text.find('a',{'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})['href']   
        try:    
            saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('₹','').replace(',','').strip())
            oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('₹','').replace(',','').strip())
            discount = (1-saleprice/oldprice)*100
        except:
            oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('₹','').replace(',','').strip())
            discount = 0


        try:
            ratings = item.find('span', {'class': 'a-size-base s-underline-text'}).text
#             print(ratings)
        except:
            ratings= 0
#             print(ratings)
        saleitem = {
                'title': title,
                'short_title': short_title,
                'link': link,
                'saleprice': saleprice,
                'oldprice': oldprice,
                'ratings': ratings            
                }
        dealslist.append(saleitem)
    return


# In[91]:


def getnextpage(soup):
    try:
        new_url = str(soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])   
        next_url = 'https://www.amazon.in/'+new_url
        return next_url
    except:
        return 


# In[92]:


while True:
    soup = getdata(url)
    getdeals(soup)
    url = getnextpage(soup)
    if not url:
        break
    else:
        print(url)
        print(len(dealslist))  


# In[ ]:


driver.quit()


# In[93]:


len(dealslist)


# In[97]:


cnt = 1
cnt = cnt+1
df = pd.DataFrame(dealslist)
df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
df = df.sort_values(by=['percentoff'], ascending=False)
df.to_csv(search_term + str(cnt) + ' -festive_deals.csv', index=False)
print('Fin.')


# In[98]:


driver.quit()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[29]:





# In[ ]:


# title = products.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'})
# print(title)


# In[ ]:


# def getdata(url):
#     r = s.get(url)
#     r.html.render(sleep=1)
#     soup = BeautifulSoup(r.html.html, 'html.parser')
#     return soup


# In[ ]:


# new_url = str(soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])   
# next_url = 'https://www.amazon.in/'+new_url
# print(next_url)


# In[ ]:


# next_url = soup.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})  
# print(next_url['href'])

