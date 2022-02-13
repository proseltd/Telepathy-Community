#!/usr/bin/env python

"""Telepathy archiving module:
    A tool for archiving Telegram chats within specific parameters.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
import details as ds
import pandas as pd
import datetime, csv, os

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

chats = []
last_date = None
chunk_size = 200
groups=[]

filetime = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")
filetime_clean = str(filetime)

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

print('Welcome to the Telepathy archiving tool. This tool will archive Telegram chats based on a list.')
user_selection_log = input('Do you want to print messages to terminal while Telepathy runs? (y/n)')
user_selection_media = input('Do you want to archive media content? (y/n)')
user_selection_date = input('Got it. Do you want to archive messages within a specific timeframe? (y/n)')
if user_selection_date == 'y':
    from_year = input('Please specify the start date (Year YYYY)')
    from_month = input('Please specify the start date (Month, without leading 0 - MM)')
    from_day = input('Please specify the start date (Day, without leading 0 - DD)')
else:
    pass

print('Archiving chats...')

async def main():
    df = pd.read_csv('to_archive.csv', sep=';')
    df = df.To.unique()

    for i in df:
        print("Working on ", i," This may take a while...")
        l = []
        try:
            async for message in client.iter_messages(i):
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

                df = pd.DataFrame(l, columns = ['Chat name','message ID','Name','ID','Message text','Message date (YYYY/MM/DD)','Message time (HH:MM)'])

                file = directory + '/'+ alphanumeric + '_' + filetime_clean +'_archive.csv'

                with open(file, 'w+') as f:
                    df.to_csv(f)

                name = get_display_name(message.sender)
                nameID = message.from_id
                year = format(message.date.year, '02d')
                month = format(message.date.month, '02d')
                day = format(message.date.day, '02d')
                hour = format(message.date.hour, '02d')
                minute = format(message.date.minute, '02d')

                date = str(year) + "/" + str(month) + "/" + str(day)
                time = str(hour) + ":" + str(minute)

                if user_selection_log == 'y':
                    print(message.id,' ',name,':',message.text,date,time)
                else:
                    pass

                if user_selection_date == 'y':
                    if (int(from_year) <= message.date.year and int(from_month) <= message.date.month and int(from_day) <= message.date.day):
                        l.append([i,message.id,name,nameID,message.text,date,time])
                    else:
                        break
                else:
                    l.append([i,message.id,name,nameID,message.text,date,time])

                if user_selection_media == 'y':
                    if message.media:
                        path = await message.download_media(file=media_directory)
                        if user_selection_log == 'y':
                            print('File saved to', path)
                        else:
                            pass
                else:
                    continue

            jsons = './json_files'
            try:
                os.makedirs(jsons)
            except FileExistsError:
                pass

            df.to_json(jsons+'/'+alphanumeric+'_archive.json',orient='split',compression='infer',index='true')

            print("Scrape completed for", i,", file saved")

            df = pd.DataFrame(None)

        except Exception as e:
            print("An exception occurred.", e)

with client:
    client.loop.run_until_complete(main())

print('List archived successfully')

again = input('Do you want to archive more groups? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("archiver.py").read())
else:
    pass

launcher = input('Do you want to return to the launcher? (y/n)')
if launcher == 'y':
    print('Restarting...')
    exec(open("telepathy.py").read())
else:
    print('Thank you for using Telepathy.')
