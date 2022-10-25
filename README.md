

Telepathy: An OSINT toolkit for investigating Telegram chats. Developed by Jordan Wildon. Version 2.2.58.


## Installation

### Pip install (recommended)

```
$ pip3 install telepathy
```

### Install from source

```
$ git clone https://github.com/jordanwildon/Telepathy.git
$ cd Telepathy
$ pip install -r requirements.txt
```

## Setup

On first use, Telepathy will ask for your Telegram API details (obtained from my.telegram.org). Once those are set up, it will prompt you to enter your phone number again and then send an authorization code to your Telegram account. If you have two-factor authentication enabled, you'll be asked to input your Telegram password.

OPTIONAL: Installing cryptg ($ pip3 install cryptg) may improve Telepathy's speed. The package hand decryption by Python over to C, making media downloads in particular quicker and more efficient. 


## Usage:

```
telepathy [OPTIONS]
```

Options:
- **'--target', '-t' [CHAT]**

this option will identify the target of the scan. The specified chat must be public. To get the chat name, look for the 't.me/chatname' link, and subtract the 't.me/'.

For example:

```
$ telepathy -t durov
```

The default is a basic scan which will find the title, description, number of participants, username, URL, chat type, chat ID, access hash, first post date and any applicable restrictions to the chat. For group chats, Telepathy will also generate a memberlist (up to 5,000 members).


- **'--comprehensive', '-c'**

A comprehensive scan will offer the same information as the basic scan, but will also archive a chat's message history.

For example:

```
$ telepathy -t durov -c
```


- **'--forwards', '-f'**

This flag will create an edgelist based on messages forwarded into a chat. It can be used alongside either a default or comprehensive scan.

For example:

```
$ telepathy -t durov -f
```


- **'--media', '-m'**

Use this flag to include media archiving alongside a comprehensive scan. This makes the process take significantly longer and should also be used with caution: you'll download all media content from the target chat, and it's up to you to not store illegal files on your system.

Since 2.2.0, downloading all media files will also generate a CSV file listing the files' metadata. 

For example, this will run a comprehensive scan, including media archiving:

```
$ telepathy -t durov -c -m
```


- **'--user', '-u' [USER]**

Looks up a specified user ID. This will only work if your account has "encountered" the user before (for example, after archiving a group), you can specify User ID or @nickname

```
$ telepathy -t 0123456789 -u

$ telepathy -t @test_user -u
```


- **'--location', '-l' [COORDINATES]**

Finds users near to specified coordinates. Input should be longitude followed by latitude, seperated by a comma. This feature only works if your Telegram account has a profile image which is set to publicly viewable.

```
$ telepathy -t 51.5032973,-0.1217424 -l
```


- **'--alt', '-a'**

Flag for running Telepathy from an alternative number. You can use the same API key and Hash but authenticate with a different phone number. Allows for running multiple scans at the same time.

```
$ telepathy -t Durov -c -a
```


- **'--export', '-e'**

Exports all chats your account is part of to a CSV file. In a future release, this may assist with setting up multiple accounts following the same groups.

```
$ telepathy -e
```
  

- **'--reply', '-r'**

Flag for enable the reply in the channel, it will map users who replied in the channel and it will dump the full conversation chain 

```
$ telepathy -t [CHANNEL] -c -r 
```


## Bonus investigations tips:

 - Navigating to a media archive directory and running Exiftool may give you a whole host of useful information for further investigation. Telegram doesn't currently scrub metadata from PDF, DOCX, XLSX, MP4, MOV and some other filetypes, which offer creation and edit time metadata, often timezones, sometimes authors, and general technical information about the perosn or people who created a media file.  
 ```
$ cd ./telepathy/telepathy_files/CHATNAME/media
$ exiftool * > metadata.txt
```
 - Group and inferred channel memberlists offer a point of further investigation for usernames found. By using Maigret, you can look up where else a username has been used. While this is not accurate in all cases, it's been proven to be useful for handles that are often reused. In this case, remember to verify your findings to avoid false positives.


## A note on how Telegram works

Telegram chats are organised into three key types: Channels, Megagroups/Supergroups and Gigagroups. Each module works slightly differently depending on the chat type. Channels can have seemingly unlimited subscribers and are where an admin will broadcast messages to an audience, Megagroups can have up to 200,000 members, each of whom can participate (if not restricted), and Gigagroups sit somewhere between the two.


## Upcoming changes
In some environments (particularly Windows), Telepathy struggles to effectively manage files and can sometimes produce errors. Fixes for these errors will come in due course.

Upcoming features include:

  - [ ] Adding a time specification flag to set archiving for specific period.
  - [ ] The ability to gather the number of reactions to messages, including statistics on engagement rate.
  - [ ] Finding a method to once again gather complete memberlists (currently restricted by the API).
  - [ ] Improved statistics: including timestamp analysis for channels.
  - [ ] Generating an entirely automated complete report, including visualisation for some statistics.
  - [ ] Hate speech analytics.
  - [x] Maximise compatibility of edgelists with Gephi.
  - [ ] Include sockpuppet account provisioning (creation of accounts from previous exported lists).
  - [ ] Listing who has group admin rights in memberlists.
  - [ ] Media downloaded in the background to increase efficiency.
  - [ ] When media archiving is flagged, the location of downloaded content will be added to the archive file.
  - [ ] Exploring, and potentially integrating, media cross checks based on https://github.com/conflict-investigations/media-search-engine.
  - [ ] Ensuring inferred channel memberlists don't contain duplicate entries.
  - [ ] Introducing local chat retrival within the location lookup module.
  - [ ] Adding trilateration option for location lookup to aid better location matching.
  - [ ] Further code refactoring to ensure long-term maintainability.
  - [ ] Progress bars for media downloads to give a better estimation of runtime.
  - [ ] Adding additional alternative logins.
  - [ ] Improved language support.
  - [ ] Ensure inferred channel memberlists (based on repliers) contains each account only once.
  - [ ] Correctly define destinction between reply (as in a chat) and comment (as in channel).


## feedback

Please send feedback to @jordanwildon on Twitter. You can follow Telepathy updates at @TelepathyDB.


## Usage terms

You may use Telepathy however you like, but your usecase is your responsibility. Be safe and respectful.


## Credits

All tools created by Jordan Wildon (@jordanwildon). Special thanks go to [Giacomo Giallombardo](https://github.com/aaarghhh) for adding additional features and code refactoring, [jkctech](https://github.com/jkctech/Telegram-Trilateration) for collaboration on location lookup via the 'People Near Me' feature, and Alex Newhouse (@AlexBNewhouse) for his help with Telepathy v1. Shoutout also to [Francesco Poldi](https://github.com/noneprivacy) for being a sounding board and offering help and advice when it comes to bug fixes.

Where possible, credit for the use of this tool in published research is desired, but not required. This can either come in the form of crediting the author, or crediting Telepathy itself (preferably with a link).
