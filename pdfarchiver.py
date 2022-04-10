#!/usr/bin/env python

"""Telepathy file archiver module:
    A tool for archiving files in a chat which may contain metadata.
"""

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
import pandas as pd
import details as ds
import getpass, csv

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.3"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

#Login details#
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

#Check authorisation#
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

print('Archiving PDFs...')

async def main():
    df = pd.read_csv('to_archive.csv', sep=';')
    df = df.To.unique()

    for i in df:
        print("Working on ", i, "...")
        l = []
        try:
            async for message in client.iter_messages(i):
                if message.forward is None:
                    if message.video is None:
                        if message.sticker is None:
                            if message.audio is None:
                                if message.voice is None:
                                    if message.document:
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

                                        path = await message.download_media(file=media_directory)
                                        print('File saved to', path)
            i_clean = i
            alphanumeric = ""
            print("Scrape completed for", i,", file saved")
        except Exception as e:
            print("An exception occurred: ", e)

with client:
    client.loop.run_until_complete(main())

print('List archived successfully')

again = input('Do you want to archive more chats? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("archiver.py").read())
else:
    pass

launcher = input('Do you want to return to the launcher? (y/n)')
if launcher == 'y':
    print('Restarting...')
    exec(open("launcher.py").read())
else:
    print('Thank you for using Telepathy.')
