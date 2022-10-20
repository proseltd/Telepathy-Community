from colorama import Fore, Back, Style
from googletrans import Translator, constants
from .const import __version__, user_agent
import requests
import textwrap
from bs4 import BeautifulSoup
import random

def print_banner():
    print(
        Fore.GREEN
        + """
          ______     __                 __  __
         /_  __/__  / /__  ____  ____ _/ /_/ /_  __  __
          / / / _ \/ / _ \/ __ \/ __ `/ __/ __ \/ / / /
         / / /  __/ /  __/ /_/ / /_/ / /_/ / / / /_/ /
        /_/  \___/_/\___/ .___/\__,_/\__/_/ /_/\__, /
                       /_/                    /____/
        -- An OSINT toolkit for investigating Telegram chats.
        -- Developed by @jordanwildon | Version """ + __version__ + """.
        """ + Style.RESET_ALL
    )

def parse_tg_date(dd):
    year = str(format(dd.year, "02d"))
    month = str(format(dd.month, "02d"))
    day = str(format(dd.day, "02d"))
    hour = str(format(dd.hour, "02d"))
    minute = str(format(dd.minute, "02d"))
    second = str(format(dd.second, "02d"))
    date = year + "-" + month + "-" + day
    mtime = hour + ":" + minute + ":" + second
    timestamp = date + "T" + mtime + "+00:00"
    return {"timestamp":timestamp, "date":date, "mtime":mtime}


def populate_user(user, group_or_chat):
    if user.username:
        username = user.username
    else:
        username = "n/a"
    if user.first_name:
        first_name = user.first_name
    else:
        first_name = ""
    if user.last_name:
        last_name = user.last_name
    else:
        last_name = ""
    if user.phone:
        phone = user.phone
    else:
        phone = "n/a"
    full_name = (first_name + " " + last_name).strip()
    return [username, full_name, user.id, phone, group_or_chat]


def process_message(mess, user_lang):

    if mess is not None:
        mess_txt = '"' + mess + '"'
    else:
        mess_txt = "none"

    if mess_txt != "none":
        translator = Translator()
        detection = translator.detect(mess_txt)
        language_code = detection.lang
        translation_confidence = detection.confidence
        translation = translator.translate(mess_txt, dest=user_lang)
        original_language = translation.src
        translated_text = translation.text
    else:
        original_language = user_lang
        translated_text = "n/a"
        translation_confidence = "n/a"

    return {
        "original_language": original_language,
        "translated_text": translated_text,
        "translation_confidence": translation_confidence,
        "message_text": mess_txt,
    }

def process_description(desc, user_lang):
    if desc is not None:
        desc_txt = '"' + desc + '"'
    else:
        desc_txt = "none"

    if desc_txt != "none":
        translator = Translator()
        detection = translator.detect(desc_txt)
        language_code = detection.lang
        translation_confidence = detection.confidence
        translation = translator.translate(desc_txt, dest=user_lang)
        original_language = translation.src
        translated_text = translation.text
    else:
        original_language = user_lang
        translated_text = "n/a"
        translation_confidence = "n/a"

    return {
        "original_language": original_language,
        "translated_text": translated_text,
        "translation_confidence": translation_confidence,
        "description_text": desc_txt,
    }

def color_print_green(first_string,second_string):
    print(
        Fore.GREEN
        + first_string
        + Style.RESET_ALL
        + second_string
    )

def parse_html_page(url):
    s = requests.Session()
    s.max_redirects = 10
    s.headers["User-Agent"] = random.choice(user_agent)
    URL = s.get(url)
    URL.encoding = "utf-8"
    html_content = URL.text
    soup = BeautifulSoup(html_content, "html.parser")
    name = ""
    group_description = ""
    total_participants = ""
    try:
        name = soup.find(
            "div", {"class": ["tgme_page_title"]}
        ).text
    except:
        name = "Not found"
    try:
        group_description = soup.find(
            "div", {"class": ["tgme_page_description"]}
        ).text
        descript = Fore.GREEN + "Description: " + Style.RESET_ALL+ group_description
        prefix = descript + " "
    except:
        group_description = "None"
        descript = Fore.GREEN + "Description: " + Style.RESET_ALL+ group_description
        prefix = descript + " "

    try:
        group_participants = soup.find(
            "div", {"class": ["tgme_page_extra"]}
        ).text
        sep = "members"
        stripped = group_participants.split(sep, 1)[0]
        total_participants = (
            stripped.replace(" ", "")
            .replace("members", "")
            .replace("subscribers", "")
            .replace("member", "")
        )
    except:
        total_participants = "Not found"  # could be due to restriction, might need to mention

    return {"name":name,"group_description":group_description, "total_participants":total_participants}