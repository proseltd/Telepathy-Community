#!/usr/bin/env python

"""Telepathy locations module:
    A tool for finding users located near given coordinates.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
from telethon import functions, types
import details as ds
import pandas as pd
import getpass

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.3"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

#Login details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

#Check authorisation
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone)
    try:
        client.sign_in(code=input('Enter code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=getpass.getpass(prompt='Password: ', stream=None)

print('Welcome to the Telegram location tool.\nThis tool will find users near a location. The tool requires your Telegram account to have a profile picture.')
lati = input('Enter the latitude:\n')
longi = input('Enter the longitude:\n')

with client:
    result = client(functions.contacts.GetLocatedRequest(
        geo_point=types.InputGeoPoint(
            lat=float(lati),
            long=float(longi),
            accuracy_radius=42
        ),
        self_expires=42
    ))
    output = result.stringify()

    f = open('locations.txt', 'w')
    print(output, file = f)

l = []
with open("locations.txt", "r") as searchfile:
  for user in searchfile:
    if "user_id=" in user:
        numeric_filter = filter(str.isdigit, user)
        ids = "".join(numeric_filter)
        l.append(ids)
        f1 = open('ids.txt', 'w')
        print(ids, file = f1)
    if "distance=" in user:
        numeric_filter = filter(str.isdigit, user)
        distance = "".join(numeric_filter)

for account in l:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))
    dialogs = client.get_dialogs()
    account = int(account)
    my_user = client.get_entity(PeerUser(account))
    print(my_user.first_name + ' with ID: ' + str(my_user.id) + ' is ' + distance + 'm from the specified coordinates.')
    f = open('userlookup.txt', 'w')
    print(my_user, file = f)

total = len(l)
print(total,'users found')
