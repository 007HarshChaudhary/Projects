# -*- coding: utf-8 -*-
"""
Created on Sat May 15 14:07:42 2021

@author: Harsh Chaudhary
"""

from twilio.rest import Client

client = Client("ACce2bbcdfcd3d439ca3f640231cffdbd2", "d6b2a6330143ec4c2ccbadfb0c229373")

call = client.calls.create(
    to = "+919540607954",
    from_=  "+12105917168",
    url='http://demo.twilio.com/docs/voice.xml'
    )

print(call.sid)

