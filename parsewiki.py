# -*- coding: utf-8 -*-
"""
Created on Wed May 11 19:20:19 2022

@author: 1
"""

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
from io import StringIO 
import io 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/1/Downloads/myastronomy-dcb28-firebase-adminsdk-6293g-48d5f19f93.json"
GOOGLE_APPLICATION_CREDENTIALS = "C:/Users/1/Downloads/myastronomy-dcb28-firebase-adminsdk-6293g-48d5f19f93.json"

try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
    firebase_admin.initialize_app(cred)

db = firestore.client()

pattern_months = '[|]\s[0-9]*\s[а-я]*\s[=]\s'
pattern_events = '\d{4}\s[—]{1}\s.*[^\n]'
pattern_events1 = '\s[*].*[^\n]'
links = [
    'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D1%8F%D0%BD%D0%B2%D0%B0%D1%80%D1%8C',
    'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D1%84%D0%B5%D0%B2%D1%80%D0%B0%D0%BB%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%BC%D0%B0%D1%80%D1%82',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%B0%D0%BF%D1%80%D0%B5%D0%BB%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%BC%D0%B0%D0%B9',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%B8%D1%8E%D0%BD%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%B8%D1%8E%D0%BB%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D1%81%D0%B5%D0%BD%D1%82%D1%8F%D0%B1%D1%80%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C',
   'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:%D0%90%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D1%8F_%D0%B4%D0%BD%D1%8F/%D0%BD%D0%BE%D1%8F%D0%B1%D1%80%D1%8C']


http = httplib2.Http()
status, response = http.request(links[1])
  
soup = BeautifulSoup(response, 'html.parser')
text = soup.get_text()
textIO = io.StringIO(text)

months = ['january',
'february',
'march', 
'april',
'may', 
'june', 
'july', 
'august', 
'september',
'october',
'november'] 
events = []
data = {}
new_line = ""
new_line1 = ""
now = ""

for line in textIO: 
    match_months = re.search(pattern_months, line)
    match_events = re.search(pattern_events, line)
    match_events1 = re.search(pattern_events1, line)
    # print(repr(line))
    if match_months:
        # Make sure to add \n to display correctly when we write it back
        
        new_line = match_months.group() 
        disallowed_characters = "|="
        for character in disallowed_characters:
        	new_line = new_line.replace(character, "")
        " ".join(new_line.split())
        # print(new_line)
        data[new_line] = []
        
    if match_events:
        # Make sure to add \n to display correctly when we write it back
        new_line1 = match_events.group()
        new_line1.strip()
        # print(new_line1)
        events.append(new_line1)
        data[new_line] += events
        events.clear()
     
        # print(events)
    if match_events1:
        new_line1 = match_events1.group()
        new_line1.strip()
        # print(new_line1)
        data[new_line] = new_line1
        events.append(new_line1)
        events.clear()
    

db.collection(u'events').document(months[10]).set(data)
print("\n NEXT MONTH ")
print(data)
    
        