#!/usr/bin/env python

"""Telepathy archiving module:
    A tool for archiving Telegram chats within specific parameters.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
from telethon import functions, types
import datetime, csv, os, getpass
import details as ds
import pandas as pd


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

print('Archiving chats...')

async def main():
    df = pd.read_csv('to_archive.csv', sep=';')
    df = df.To.unique()

    for i in df:
        print("Working on ",i," This may take a while...")
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

                        file = directory + '/'+ alphanumeric + '_' + filetime_clean +'_archive.csv'

                        with open(file, 'w+') as f:
                            df.to_csv(f, sep=';')

                        name = get_display_name(message.sender)
                        nameID = message.from_id
                        year = str(format(message.date.year, '02d'))
                        month = str(format(message.date.month, '02d'))
                        day = str(format(message.date.day, '02d'))
                        hour = str(format(message.date.hour, '02d'))
                        minute = str(format(message.date.minute, '02d'))
                        reply = message.reply_to_msg_id
                        views = int(message.views)
                        forward_ID = message.fwd_from.from_id
                        forward_name = message.fwd_from.from_name
                        forward_post_ID = int(message.fwd_from.channel_post)
                        post_author = message.fwd_from.post_author

                        date = year + "-" + month + "-" + day
                        time = hour + ":" + minute
                        timestamp = date + ', ' + time

                        if user_selection_log == 'y':
                            print(name,':','"' + message.text + '"',timestamp)
                        else:
                            pass

                        l.append([i,message.id,name,nameID,'"' + message.text + '"',timestamp,reply,views,forward_ID,forward_name,post_author,forward_post_ID])
                        if user_selection_media == 'y':
                            if message.media:
                                path = await message.download_media(file=media_directory)
                                if user_selection_log == 'y':
                                    print('File saved to', path)
                            else:
                                pass

                    except:
                        continue
                else:
                    l.append(['None','None','None','None','None','None','None','None','None','None','None','None','None'])
                    continue

            jsons = './json_files'
            try:
                os.makedirs(jsons)
            except FileExistsError:
                pass

            df.to_json(jsons+'/'+alphanumeric+'_archive.json',orient='split',compression='infer',index='true')

            print("Scrape completed for",i,", file saved")

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
