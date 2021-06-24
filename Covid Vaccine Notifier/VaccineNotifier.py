# -*- coding: utf-8 -*-
"""
Created on Sat May 15 15:04:27 2021

@author: Harsh Chaudhary
"""

import urllib.request
import json
import datetime
import time

from twilio.rest import Client

date_object = datetime.datetime.now()
date = str(date_object.day) + "-" + str(date_object.month) + "-" + str(date_object.year)

api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"

bhiwadi = api.format("301019", date)

request = urllib.request.Request(bhiwadi, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}) 

def getData(hits):
    try:
        response = urllib.request.urlopen(request).read()
        data = json.loads(response)
        for center in data['centers']:
            for session in center['sessions']:
                if session['available_capacity'] > 1 and session['min_age_limit'] == 18:
                    hits.append({'name': center['name'], 'date': session['date'], 'available_capacity': session['available_capacity']})
        return hits
    except Exception as e:
        print("Some error occured: ", str(e))
        return None

def callMe(hits):
    client = Client("ACce2bbcdfcd3d439ca3f640231cffdbd2", "d6b2a6330143ec4c2ccbadfb0c229373")

    txt = "Found {} centers:".format(len(hits))
    for center in hits:
        txt += '''\n{} | {} | Quantity: {}'''.format(center['name'], center['date'], center['available_capacity'])

    client.messages.create(
        to = "+919540607954",
        from_ =  "+12105917168",
        body = txt
    )
    client.messages.create(
        to = "+918949449021",
        from_ =  "+12105917168",
        body = txt
    )

while True:
    
    hits = []
    flag = False
    response = getData(hits)
    if response is not None and len(response)>0:
        flag = True
    else:
        print("Trying again ...")
        time.sleep(3)        
    
    while flag:    
        if response:
            print('found slots, Check your message box ...')
            callMe(hits)
            flag = False
            time.sleep(60*2)



        
        
    

