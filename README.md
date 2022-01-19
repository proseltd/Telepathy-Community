# Telepathy

Welcome to Telepathy, an OSINT toolkit for scraping Telegram data to help investigate shady goings on.

## Installation

1. Install from source

```
git clone https://github.com/jordanwildon/Telepathy.git
cd Telepathy
pip install -r requirements.txt
```

2. Register for and obtain your Telegram API details from [my.telegram.org][1].

3. Navigate to the installation directory and run setup.py, this will walk you through the Telegram API login and prepare the toolkit with your details.

```
python3 setup.py
```

## Usage

Upon installation completion, you will be able to launch telepathy.py. On first use of any of the modules, Telepathy will ask you for an authorization code that will be sent to your Telegram account.

_telepathy.py_

A launcher to select which module you would like to use.

_archiver.py_

This module batch archives the entirety of the chats you specify in _to_archive.csv_ (this must have only one column with "To" as the header). Messages are archives in both .CSV and .JSON formats and media content (photos, videos and documents) is saved to the directory Telepathy is installed in. For the module to work, the chat has to either be public, or your Telegram account needs to be a member. The module can also be set to run on a cron job to regularly archive target chats. Please use responsibly.

Tip: Comment out the three lines of code below to skip archiving of media content. Uncomment line 82 and/or 87 to show messages in the terminal and/or directory of saved media.

```
#if message.media:
#  path = await message.download_media()
#  print('File saved to', path)
```

_members.py_

This module scrapes the memberlist of a group your Telegram account is a member of. This works best with aged accounts and once the Telegram client has 'seen' members before. The module will still operate without these conditions, but 'invisible' members might not be saved to the memberlist.

_forwards.py_

This module scrapes the names of chats that have had messages forwarded into your target groups and automatically save these in an edgelist named _edgelist.csv_. It can then scrape forwards from all the discovered channels for a larger network map, which is saved as _net.csv_. This second feature takes a long time to run, but is worthwhile for a broader analysis. This edglist can then be used with software such as Gephi to visualize the network you have discovered.

Tip: Forwards module runs silently by defaut, uncomment line 30 and 91 to print source and target of forwarded messages.


## A note on how Telegram works

Telegram chats are organised into two [key types][2]: channels and megagroups/supergroups. Each module works slightly differently depending on the chat type. For example, subscribers of Channels can't be scraped with the _members.py_ module. Channels can have seemingly unlimited subscribers, megagroups can have up to 200,000 members.

## Feedback

Please send feedback to @[jordanwildon][3] on Twitter

## Usage terms

You may use Telepathy however you like, but your usecase is your responsibility. Be safe and respectful.

## Credits

All tools created by Jordan Wildon (@[jordanwildon][3]) with some suggestions, improvements and bug-busting contributed by Alex Newhouse (@[AlexBNewhouse][4]).

Where possible, credit for the use of this tool in published research is desired, but not required.

[1]: <https://my.telegram.org/auth?to=apps> "Telegram API"
[2]: <https://core.telegram.org/api/channel> "Telegram chat types"
[3]: <https://www.twitter.com/jordanwildon> "@jordanwildon"
[4]: <https://www.twitter.com/AlexBNewhouse> "@AlexBNewhouse"
