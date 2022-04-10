#!/usr/bin/env python

"""Telepathy user lookup module:
    A tool for getting information on a Telegram account by searching the user ID
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
import details as ds

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.3"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

dialogs = client.get_dialogs()

while True:
    try:
        user = input("Please enter a Telegram user ID:\n")
        print(f'You entered "{user}"')
        answer = input('Is this correct? (y/n)')
        if answer == 'y':
            print('Finding information about:', user,'...')
            break;
    except:
            continue

user = int(user)

my_user = str(client.get_entity(PeerUser(user)))
my_user = my_user.replace(",", "\n")
print(my_user)
