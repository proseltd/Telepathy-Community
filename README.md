# Telepathy

Welcome to Telepathy, an OSINT toolkit for scraping Telegram data to help investigate shady goings on. Currently, the tool is limited to scraping only the sources of forwarded messages. Its capabilities will be increased over time.

## Installation

1. Install from source

```bash
git clone https://github.com/jordanwildon/Telepathy.git
pip install -r requirements.txt
```

2. Register for and obtain your Telegram API details from [my.telegram.org][1].

3. Navigate to the installation directory and run setup.py, this will walk you through the Telegram API login and prepare the toolkit with your details.

```bash
python3 setup.py
```

## Usage

Upon installation completion, you will be able to launch forwards.py. On first use, it will ask you for an authorization code that will be sent to your Telegram account.

_The Telegram forwards scraper_
This tool scrapes the names of chats that have had messages forwarded into your target groups and automatically save these in an edgelist named _edgelist.csv_. It can then scrape forwards from all the discovered channels for a larger network map, which is saved as _net.csv_. This second feature takes a long time to run, but is worthwhile for a broader analysis. This edglist can then be used with software such as Gephi to visualize the network you have discovered.

## Feedback

Please send all feedback either to (@[jordanwildon][2]) on Twitter

## Usage terms

You may use Telepathy however you like, however how you use the tool is your responsibility. Be safe and respectful.

## Credits

All tools created by Jordan Wildon (@[jordanwildon][2]) with some suggestions, improvements and bug-busting contributed by Alex Newhouse (@[AlexBNewhouse][3]).

Where possible, credit for the use of this tool in published research is desired, but not required.

[1]: <https://my.telegram.org/auth?to=apps> "Telegram API"
[2]: <https://www.twitter.com/jordanwildon> "@jordanwildon"
[3]: <https://www.twitter.com/AlexBNewhouse> "@AlexBNewhouse"
