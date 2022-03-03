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
import pandas as pd

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.1"
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

async def main():
    df = pd.read_csv('sourcelist.csv', sep=';')
    l = (df['To'].to_list())
    # l = (df['ID'].to_list())
    for i in l:
            try:
                ent = await client.get_entity(i)
                username = ent.username
                print("https://t.me/" + username)

            except Exception as e:
                substring = "Cannot find any entity"
                if substring in str(e):
                    print("Entity not found for " + i)
                else:
                    print("An exception occurred.", e)

with client:
    client.loop.run_until_complete(main())
