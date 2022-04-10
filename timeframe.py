#!/usr/bin/env python

"""Telepathy archiving module:
    A tool for archiving Telegram chats within specific parameters.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors import SessionPasswordNeededError
from datetime import date, datetime, timedelta
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import datetime, csv, os
import details as ds
import pandas as pd
import numpy as np
import getpass

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
    client.sign_in(phone)
    try:
        client.sign_in(code=input('Enter code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=getpass.getpass(prompt='Password: ', stream=None))

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    groups.append(chat)

filetime = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")
filetime_clean = str(filetime)

from_year = input('Please specify the start date (Year YYYY)')
from_month = input('Please specify the start date (Month, without leading 0 - MM)')
from_day = input('Please specify the start date (Day, without leading 0 - DD)')
dt_start = from_year + ',' + from_month + ',' + from_day
d_start = datetime.datetime.strptime(dt_start, '%Y,%m,%d')

to_year = input('Please specify the end date (Year YYYY)')
to_month = input('Please specify the end date (Mon th, without leading 0 - MM)')
to_day = input('Please specify the end date (Day, without leading 0 - DD)')
dt_end = to_year + ',' + to_month + ',' + to_day
d_end = datetime.datetime.strptime(dt_end, '%Y,%m,%d')

print('Archiving chats...')

async def main():
    df = pd.read_csv('to_archive.csv', sep=';')
    df = df.To.unique()

    for i in df:
        print("Working on ",i)
        l = []
        try:
            async for message in client.iter_messages(i):
                if message is not None:
                    try:
                        i_clean = i
                        alphanumeric = ""

                        for character in i_clean:
                            if character.isalnum():
                                alphanumeric += character
                        directory = './' + alphanumeric

                        try:
                            os.makedirs(directory)
                        except FileExistsError:
                            pass
                        media_directory = directory + '/media'

                        try:
                            os.makedirs(media_directory)
                        except FileExistsError:
                            pass

                        df = pd.DataFrame(l, columns = ['Chat name','message ID','Name','ID','Message text','Timestamp','Reply to','Views','Forward Peer ID','Forwarded From','Post Author','Forward post ID'])

                        name = get_display_name(message.sender)
                        nameID = message.from_id
                        year = str(format(message.date.year, '02d'))
                        month = str(format(message.date.month, '02d'))
                        day = str(format(message.date.day, '02d'))
                        hour = str(format(message.date.hour, '02d'))
                        minute = str(format(message.date.minute, '02d'))

                        datestamp = year + "," + month + "," + day
                        datestamp_clean = datetime.datetime.strptime(datestamp, '%Y,%m,%d')
                        timestamp = year + "-" + month + "-" + day + ", " + hour + ":" + minute

                        if d_start <= datestamp_clean: #and d_end >= datestamp_clean:
                            l.append([i,message.id,name,nameID,'"' + message.text + '"',timestamp,reply,views,forward_ID,forward_name,post_author,forward_post_ID])
                            print(i,message.id,name,nameID,'"' + message.text + '"',timestamp)
                            #if message.media:
                            #    path = await message.download_media(file=media_directory)
                            file = directory + '/'+ alphanumeric + '_' + filetime_clean +'_archive.csv'

                            with open(file, 'w+') as f:
                                df.to_csv(f, sep=';')
                        else:
                            break
                    except:
                        continue
                else:
                    l.append(['None','None','None','None','None','None','None','None','None','None','None','None','None'])
                    continue

        except Exception as e:
            print("An exception occurred.", e)

        print("Scrape completed for",i,", file saved")

with client:
    client.loop.run_until_complete(main())
