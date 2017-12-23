# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 23:41:37 2017

@author: Minkush
"""

import bs4
import requests
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def scrape(q):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    query = "https://www.quora.com/search?q="+q

    res = requests.get(query,headers = headers)

    res.raise_for_status

    soup = bs4.BeautifulSoup(res.text,'html.parser')
    text = soup.find_all(text=True)
    visible_texts = filter(tag_visible, text)
    contentofthepage = u" ".join(t.strip() for t in visible_texts)
    return contentofthepage

tags = str(input())
contentOfThePage = scrape(tags)

   
