from telethon import TelegramClient
from telethon import utils
import pandas as pd
import details as ds
import os

#Login details#
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

print('Welcome to channel forward scraper.\nThis tool will scrape a Telegram channel for all forwarded messages and their original sources.')

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
                    #print(ent.title,">>>",channel_name)
                    df = pd.DataFrame(l, columns = ['To','From'])

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

                    l.append([channel_name, ent.title])

            except:
              #print("An exception occurred: Could be private, now deleted, or a group.")
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
                            #print(ent.title,">>>",i)

                            df = pd.DataFrame(l, columns = ['To','From'])

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

                            l.append([i, ent.title])
                    except:
                        #print("An exception occurred: Could be private, now deleted, or a group.")
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
