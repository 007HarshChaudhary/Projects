# -*- coding: utf-8 -*-
"""
Created on Sat May 15 12:34:53 2021

@author: Harsh Chaudhary
"""
import urllib.request
import json
import datetime

dist_to_id = {
    'Alwar': '512',
    'Rewari': '202',
    'Gurgaon': '188',    
    }

district_id = '512'
date_object = datetime.datetime.now()
date = str(date_object.day) + "-" + str(date_object.month) + "-" + str(date_object.year)
api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"

alwar = api.format(dist_to_id['Alwar'], date)
rewari = api.format(dist_to_id['Rewari'], date)
gurgaon = api.format(dist_to_id['Gurgaon'], date)

request_alwar = urllib.request.Request(alwar, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'})
request_rewari = urllib.request.Request(rewari, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'})
request_gurgaon = urllib.request.Request(gurgaon, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'})

response_alwar = urllib.request.urlopen(request_alwar).read()
response_rewari = urllib.request.urlopen(request_rewari).read()
response_gurgaon = urllib.request.urlopen(request_gurgaon).read()
responses = [response_alwar, response_rewari, response_gurgaon]

hits = []
    
for response in responses:
    data = json.loads(response)
    for center in data['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                hits.append(center['name'] + " --> " + center['district_name'] + " --> " + session['date'])

