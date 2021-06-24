# -*- coding: utf-8 -*-
"""
Created on Sat May 15 14:18:06 2021

@author: Harsh Chaudhary
"""

import smtplib
from email.message import EmailMessage

hits = [{'name': 'Harsh'}, {'name': 'Om'}]
msg = EmailMessage()
msg['Subject'] = 'Vaccine available'
msg['From'] = "theheroisbackagain@gmail.com"
msg['To'] = "theheroisbackagain@gmail.com"
body = ''
for center in hits:
    body += '''\n{}'''.format(center['name'])
msg.set_content(body)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('theheroisbackagain@gmail.com', 'hejwshhzzulkrbho')
   
    smtp.send_message(msg)

