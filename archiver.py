#Imports#
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.utils import get_display_name
import pandas as pd
import details as ds
import csv

#Login details#
api_id = ds.apiID
api_hash = ds.apiHash
phone = ds.number
client = TelegramClient(phone, api_id, api_hash)

#Check authorisation#
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

#chatlist.csv to be replaced with your list of channels, must have "To" as a column header#

async def main():
    df = pd.read_csv('to_archive.csv')
    df = df.To.unique()

    for i in df:
        print("Working on ", i, "...")
        l = []
        try:
            async for message in client.iter_messages(i):
                name = get_display_name(message.sender)
                nameID = message.from_id
                date = str(message.date.year) + "/" + str(message.date.month) + "/" + str(message.date.day)
                time = str(message.date.hour) + ":" + str(message.date.minute)
                timestamp = date + ", " + time
                #print(message.id,' ',name,':',message.text)
                l.append([i,message.id,name,nameID,message.text,timestamp])

                if message.media:
                    path = await message.download_media()
                    print('File saved to', path)

            df = pd.DataFrame(l, columns = ['Chat name','message ID','Name','ID','Message text','Message date and time (YYYY/MM/DD, HH:MM)'])

            i_clean = i
            alphanumeric = ""

            for character in i_clean:
                if character.isalnum():
                    alphanumeric += character

            df.to_csv(alphanumeric + '_archive.csv')
            df.to_json(alphanumeric + '_archive.json', orient = 'split', compression = 'infer', index = 'true')

            print("Scrape completed for", i,", file saved")

            df = pd.DataFrame(None)

        except Exception as e:
            print("An exception occurred.", e)


with client:
    client.loop.run_until_complete(main())

print('List archived successfully')
print('Thank you for using Telepathy.')
