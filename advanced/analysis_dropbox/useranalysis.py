
"""Telepathy archiving module:
    A tool for archiving Telegram chats within specific parameters.
"""

import pandas as pd
import glob

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.0.1"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

print('Welcome to the Telepathy post frequency analysis tool. \nThis tool calculates the most common posters among one or a set of Telegram group archives.')

df = pd.concat(map(pd.read_csv, glob.glob('*archive.csv')))
pd.set_option("display.max_rows", df.shape[0]+1, "display.max_columns", 3)
count = df.ID.count()
value_count = df['ID'].value_counts()
print(value_count)

df = df.ID.unique()
length = len(df)
print(length,'people have posted',count,'times in the group(s).')
