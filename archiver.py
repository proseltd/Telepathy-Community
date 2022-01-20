#Imports
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
import pandas as pd
import details as ds
import csv
import os

#Login details
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

#Check authorisation
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

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

print('Archiving chats...')

#to_archive.csv to be replaced with your list of channels, must have "To" as a column header#

async def main():
    df = pd.read_csv('to_archive.csv')
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

                df = pd.DataFrame(l, columns = ['Chat name','message ID','Name','ID','Message text','Message date and time (YYYY/MM/DD, HH:MM)'])

                file = directory + '/'+ alphanumeric + '_archive.csv'

                with open(file, 'w+') as f:
                    df.to_csv(f, header=False)

                name = get_display_name(message.sender)
                nameID = message.from_id
                date = str(message.date.year) + "/" + str(message.date.month) + "/" + str(message.date.day)
                time = str(message.date.hour) + ":" + str(message.date.minute)
                timestamp = date + ", " + time
                #print(message.id,' ',name,':',message.text)
                l.append([i,message.id,name,nameID,message.text,timestamp])

                if message.media:
                    path = await message.download_media(file=media_directory)
                    #print('File saved to', path)

            df.to_json(directory + alphanumeric + '_archive.json', orient = 'split', compression = 'infer', index = 'true')

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
