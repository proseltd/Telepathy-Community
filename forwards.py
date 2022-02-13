#!/usr/bin/env python

"""Telepathy forward scraping module:
    A tool for creating an edgelist of forwarded messages.
"""

from telethon import TelegramClient
from telethon import utils
import pandas as pd
import details as ds
import os

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

print('Welcome to channel forward scraper.\nThis tool will scrape a Telegram channel for all forwarded messages and their original sources.')
user_selection_log = input('Do you want to print forwards to terminal while Telepathy runs? (y/n)')

while True:
    try:
        channel_name = input("Please enter a Telegram channel name:\n")
        print(f'You entered "{channel_name}"')
        answer = input('Is this correct? (y/n)')
        if answer == 'y':
            print('Scraping forwards from', channel_name, 'This may take a while...')
            break;
    except:
            continue

async def main():
    l = []
    async for message in client.iter_messages(channel_name):

        if message.forward is not None:
            try:
                id = message.forward.original_fwd.from_id
                if id is not None:
                    ent = await client.get_entity(id)
                    name = get_display_name(message.sender)
                    nameID = message.from_id
                    year = format(message.date.year, '02d')
                    month = format(message.date.month, '02d')
                    day = format(message.date.day, '02d')
                    hour = format(message.date.hour, '02d')
                    minute = format(message.date.minute, '02d')

                    date = str(year) + "/" + str(month) + "/" + str(day)
                    time = str(hour) + ":" + str(minute)
                    if user_selection_media == 'y':
                        print(ent.title,">>>",channel_name)
                    else:
                        pass
                    df = pd.DataFrame(l, columns = ['To','From','date','time'])

                    name_clean = channel_name
                    alphanumeric = ""

                    for character in name_clean:
                        if character.isalnum():
                            alphanumeric += character

                    directory = './edgelists/'
                    try:
                        os.makedirs(directory)
                    except FileExistsError:
                        pass

                    file = './edgelists/'+ alphanumeric + '_edgelist.csv'

                    with open(file,'w+') as f:
                        df.to_csv(f)

                    l.append([channel_name, ent.title, date, time])

            except:
                if user_selection_media == 'y':
                    print("An exception occurred: Could be private, now deleted, or a group.")
                else:
                    pass

with client:
    client.loop.run_until_complete(main())

print('Forwards scraped successfully.')

next1 = input('Do you also want to scrape forwards from the discovered channels? (y/n)')
if next1 == 'y':
    print('Scraping forwards from channels discovered in', channel_name, '...')
    async def new_main():
        name_clean = channel_name
        alphanumeric = ""

        for character in name_clean:
            if character.isalnum():
                alphanumeric += character
        df = pd.read_csv('./edgelists/'+ alphanumeric + '_edgelist.csv')
        df = df.From.unique()
        l = []
        for i in df:
            async for message in client.iter_messages(i):
                if message.forward is not None:
                    try:
                        id = message.forward.original_fwd.from_id
                        if id is not None:
                            ent = await client.get_entity(id)
                            year = format(message.date.year, '02d')
                            month = format(message.date.month, '02d')
                            day = format(message.date.day, '02d')
                            hour = format(message.date.hour, '02d')
                            minute = format(message.date.minute, '02d')

                            date = str(year) + "/" + str(month) + "/" + str(day)
                            time = str(hour) + ":" + str(minute)

                            if user_selection_media == 'y':
                                print(ent.title,">>>",i)
                            else:
                                pass

                            df = pd.DataFrame(l, columns = ['To','From','date','time'])

                            name_clean = channel_name
                            alphanumeric = ""

                            for character in name_clean:
                                if character.isalnum():
                                    alphanumeric += character

                            directory = './edgelists/'
                            try:
                                os.makedirs(directory)
                            except FileExistsError:
                                pass

                            file1 = './edgelists/'+ alphanumeric + '_net.csv'

                            with open(file1,'w+') as f:
                                df.to_csv(f)

                            l.append([i, ent.title, date, time])
                    except:
                        if user_selection_media == 'y':
                            print("An exception occurred: Could be private, now deleted, or a group.")
                        else:
                            pass

            print("Scrape complete for:", i,)
        df.to_json(alphanumeric + '_archive.json', orient = 'split', compression = 'infer', index = 'true')

    with client:
        client.loop.run_until_complete(new_main())
    print('Forwards scraped successfully.')
else:
    pass

again = input('Do you want to scrape more chats? (y/n)')
if again == 'y':
    print('Restarting...')
    exec(open("forwards.py").read())
else:
    pass

launcher = input('Do you want to return to the launcher? (y/n)')
if launcher == 'y':
    print('Restarting...')
    exec(open("telepathy.py").read())
else:
    print('Thank you for using Telepathy.')
