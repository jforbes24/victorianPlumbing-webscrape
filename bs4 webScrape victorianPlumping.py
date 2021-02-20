import requests
import bs4
import lxml
import random
import numpy as np
import pandas as pd
import re
import time
import os

# assign user-agent
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    ]

catLinks = []
brickLinks = []
productLinks = []
nestedLinks = []

# pick a random user agent
for i in range(1,6):
    user_agent = random.choice(user_agent_list)
    # set the headers
    headers = {'User-Agent' : user_agent}


# get category pages
baseurl = 'https://www.victorianplumbing.co.uk'

result = requests.get(baseurl, headers=headers)
soup = bs4.BeautifulSoup(result.content, 'lxml')
megaMenu = soup.find('div', class_='main-nav')

try:
    for cat in megaMenu.find_all('a', href=True):
        if baseurl + cat['href'] in catLinks:
            continue
        else:
            catLinks.append(baseurl + cat['href'])
        time.sleep(0.5)
    print(len(catLinks))
except Exception as ex:
    print('Error: ', ex)

# get nested links
try:
    for nextPage in catLinks:
        result = requests.get(nextPage, headers=headers)
        broth = bs4.BeautifulSoup(result.content, 'lxml')

        # get nested page links
        try:
            for urlLink in broth.find_all('a', class_='next-arrow'):
                if baseurl + urlLink['href'] in catLinks:
                    continue
                else:
                    catLinks.append(baseurl + urlLink['href'])
                    print(len(catLinks))
                time.sleep(0.5)
        except:
            continue
except Exception as ex:
    print('Error: ', ex)

# get products

try:
    for product in catLinks:
        result = requests.get(product, headers=headers)
        soup = bs4.BeautifulSoup(result.content, 'lxml')
        products = soup.find_all('div', class_='prod-box')

        # get product links
        for item in products:
            for link in item.find_all('a', href=True):
                if (link['href'] != "javascript:void(0);" and (baseurl + link['href'] not in productLinks)):
                    productLinks.append(baseurl + link['href'])
                else:
                    continue
                print(len(productLinks))
                time.sleep(0.5)
except Exception as ex:
    print('Error: ', ex)


# test
test = 'https://www.victorianplumbing.co.uk/mira-coda-pro-ev-thermostatic-bar-shower-mixer-chrome-1-1836-005'

productData = []

try:
    for link in productLinks:
        # get product attributes
        result = requests.get(link, headers=headers)
        soup = bs4.BeautifulSoup(result.content, 'lxml')
        products = soup.find('div', class_='prod-box')

        

        # get SKU
        try:
            sku = soup.select('#lblProdCodeMain')[0].text.strip()
        except:
            sku = 'na'

        # get name
        try:
            name = soup.find('h1').text
        except:
            name = 'na'

        # get category
        try:
            category = soup.select('#Breadcrumb')[0].find_all('span')[2].text.strip()
        except:
            category = 'na'

        # get subCategory
        try:
            subCat = soup.select('#Breadcrumb')[0].find_all('span')[3].text.strip()
        except:
            subCat = 'na'

        # get subSubCategory
        try:
            subSubCat = soup.select('#Breadcrumb')[0].find_all('span')[5].text.strip()
        except:
            subSubCat = 'na'

        # get rating
        try:
            rating = float(soup.find_all('div', class_='overallRatingBox')[0].find_all('span')[2].text.strip(' out of 5'))
        except:
            rating = 0

        # totalReviews
        try:
            totalReviews = int(soup.find_all('a', class_='pdReadReviewLink')[1].text.strip(' Reviews'))
        except:
            totalReviews = 0

        # reviews
        try:
            reviews = soup.find_all('div', class_='reviewsummary')[0].text.strip()
        except:
            reviews = 'no reviews'

        # get price
        try:
            price = float(soup.find('span', itemprop='price').text.strip())
        except:
            price = 'na'

        # get was price
        try:
            wasPrice = float(soup.find('span', class_='pordRRPPrice').text.strip()[5:])
        except:
            wasPrice = 'na'
        
        # get availability
        try:
            availability = soup.find('div', class_='pordInStock').text.strip()
        except:
            availability = 'na'

        # get lead time
        try:
            leadTime = soup.find('span', class_='ETAperiod').text.strip()
        except:
            leadTime = "na"

        # get images
        try:
            container = soup.find_all('img')
            images = 0
            for image in container:
                if (image.get('data-big')) == None:
                    continue
                else:
                    images = images + 1
        except:
            images = 'na'

        # create sku dictionary
        try:
            sku = {'sku' : sku,
                   'description' : name,
                   'price' : price,
                   'wasPrice' : wasPrice,
                   'category' : category,
                   'subCat' : subCat,
                   'subSubCat' : subSubCat,
                   'rating' : rating,
                   'totalReviews' : totalReviews,
                   'reviews' : reviews,
                   'availability' : availability,
                   'leadTime' : leadTime,
                   'images' : images,
                   'link' : link
                   }
            if sku in productData:
                continue
            else:
                productData.append(sku)
        except Exception as ex:
            print('Error: ', ex)

        time.sleep(0.5)

        print(len(productData))
              
except Exception as ex:
    print('Error: ', ex)

# create dataframe
df = pd.DataFrame(productData)

# save to excel
df.to_excel(r'C:\\Users\\forbej06\\OneDrive - Kingfisher PLC\\dev\\Range\\VictorianPlumping\\bs4victorianPlumbing.xlsx')

print(df)
