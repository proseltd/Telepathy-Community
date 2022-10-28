from colorama import Fore, Style
from googletrans import Translator
from telepathy.const import __version__, user_agent
import requests
import textwrap
from bs4 import BeautifulSoup
import random

def createPlaceholdeCls():
    class Object(object):
        pass
    a = Object()
    return a

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
        username = "N/A"
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
        phone = "N/A"
    if user.id:
        user_id = user.id
    else:
        user_id = "N/A"
    full_name = (first_name + " " + last_name).strip()
    return [username, full_name, user_id, phone, group_or_chat]


def process_message(mess, user_lang):

    if mess is not None:
        mess_txt = '"' + mess + '"'
    else:
        mess_txt = "None"

    if mess_txt != "None":
        translator = Translator()
        detection = translator.detect(mess_txt)
        translation_confidence = detection.confidence
        translation = translator.translate(mess_txt, dest=user_lang)
        original_language = translation.src
        translated_text = translation.text
    else:
        original_language = user_lang
        translated_text = "N/A"
        translation_confidence = "N/A"

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
        desc_txt = "None"

    if desc_txt != "None":
        translator = Translator()
        detection = translator.detect(desc_txt)
        translation_confidence = detection.confidence
        translation = translator.translate(desc_txt, dest=user_lang)
        original_language = translation.src
        translated_text = translation.text
    else:
        original_language = user_lang
        translated_text = "N/A"
        translation_confidence = "N/A"

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
    except:
        group_description = "None"
        descript = Fore.GREEN + "Description: " + Style.RESET_ALL+ group_description

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
        total_participants = "Not found"

    return {"name":name,"group_description":group_description, "total_participants":total_participants}


def generate_textwrap(text_string, size=70):
    trans_descript = Fore.GREEN + f"{text_string} " + Style.RESET_ALL
    prefix = trans_descript
    return textwrap.TextWrapper(
        initial_indent=prefix,
        width=size,
        subsequent_indent="                  ",
    )

def print_shell(type, obj):
    if type == "user":
        color_print_green(" [+] ", "User details for " + obj.target)
        color_print_green("  ├  Username: ", str(obj.username))
        color_print_green("  ├  Name: ", str(obj.user_full_name))
        color_print_green("  ├  Verification: ", str(obj.verified))
        color_print_green("  ├  Photo ID: ", str(obj.user_photo))
        color_print_green("  ├  Phone number: ", str(obj.phone))
        color_print_green(
            "  ├  Access hash: ", str(obj.access_hash)
        )
        color_print_green("  ├  Language: ", str(obj.lang_code))
        color_print_green("  ├  Bot: ", str(obj.bot))
        color_print_green("  ├  Scam: ", str(obj.scam))
        color_print_green("  ├  Last seen: ", str(obj.user_status))
        color_print_green("  └  Restrictions: ", str(obj.user_restrictions))

    if type == "location_report":
        color_print_green(" [+] Users located", "")
        color_print_green("  ├  Users within 500m:  ", str(obj.d500))
        color_print_green("  ├  Users within 1000m: ", str(obj.d1000))
        color_print_green("  ├  Users within 2000m: ", str(obj.d2000))
        color_print_green("  ├  Users within 3000m: ", str(obj.d3000))
        color_print_green("  ├  Total users found:  ", str(obj.total))
        color_print_green("  └  Location list saved to: ", obj.save_file)

    if type == "channel_recap" or type == "group_recap":

        d_wrapper = generate_textwrap("Description:")
        td_wrapper = generate_textwrap("Translated Description:")

        color_print_green("  ┬  Chat details", "")
        color_print_green("  ├  Title: ", str(obj.title))
        color_print_green("  ├  ", d_wrapper.fill(obj.group_description))
        if obj.translated_description != obj.group_description:
            color_print_green("  ├  ", td_wrapper.fill(obj.translated_description))
        color_print_green(
            "  ├  Total participants: ", str(obj.total_participants)
        )

        if type == "group_recap":
            color_print_green(
                "  ├  Participants found: ",
                str(obj.found_participants)
                + " ("
                + str(format(obj.found_percentage, ".2f"))
                + "%)",
            )

        color_print_green("  ├  Username: ", str(obj.group_username))
        color_print_green("  ├  URL: ", str(obj.group_url))
        color_print_green("  ├  Chat type: ", str(obj.chat_type))
        color_print_green("  ├  Chat id: ", str(obj.id))
        color_print_green("  ├  Access hash: ", str(obj.access_hash))
        if type ==  "channel_recap":
            scam_status = str(obj.scam)
            color_print_green("  ├  Scam: ", str(scam_status))
        color_print_green("  ├  First post date: ", str(obj.first_post))
        if type == "group_recap":
            color_print_green(
                "  ├  Memberlist saved to: ", obj.memberlist_filename
            )
        color_print_green(
            "  └  Restrictions: ", (str(obj.group_status))
        )

    if type == "group_stat":
        color_print_green(" [+] Chat archive saved", "")
        color_print_green("  ┬  Chat statistics", "")
        color_print_green(
            "  ├  Number of messages found: ", str(obj.messages_found)
        )
        color_print_green(
            "  ├  Top poster 1: ", str(obj.poster_one)
        )
        color_print_green(
            "  ├  Top poster 2: ", str(obj.poster_two)
        )
        color_print_green(
            "  ├  Top poster 3: ", str(obj.poster_three)
        )
        color_print_green(
            "  ├  Top poster 4: ", str(obj.poster_four)
        )
        color_print_green(
            "  ├  Top poster 5: ", str(obj.poster_five)
        )
        color_print_green(
            "  ├  Total unique posters: ", str(obj.unique_active)
        )
        color_print_green(
            "  └  Archive saved to: ", str(obj.file_archive)
        )
        return

    if type == "channel_stat":
        color_print_green(" [+] Channel archive saved", "")
        color_print_green("  ┬  Channel statistics", "")
        color_print_green(
            "  ├  Number of messages found: ", str(obj.messages_found)
        )
        color_print_green(
            "  └  Archive saved to: ", str(obj.file_archive)
        )
        return

    if type == "reply_stat":
        middle_char = "├"
        if obj.user_replier_list_len == 0:
            middle_char = "└"

        color_print_green(" [+] Replies analysis ", "")
        color_print_green("  ┬  Chat statistics", "")
        color_print_green(
            f"  {middle_char}  Archive of replies saved to: ",
            str(obj.reply_file_archive),
        )
        if obj.user_replier_list_len > 0:
            color_print_green(
                "  └  Active members list who replied to messages, saved to: ",
                str(obj.reply_memberlist_filename),
            )
        color_print_green(
            "  ┬  Top replier 1: ", str(obj.replier_one)
        )
        color_print_green(
            "  ├  Top replier 2: ", str(obj.replier_two)
        )
        color_print_green(
            "  ├  Top replier 3: ", str(obj.replier_three)
        )
        color_print_green(
            "  ├  Top replier 4: ", str(obj.replier_four)
        )
        color_print_green(
            "  ├  Top replier 5: ", str(obj.replier_five)
        )
        color_print_green(
            "  └   Total unique repliers: ", str(obj.replier_unique)
        )

    if type == "forwarder_stat":
        color_print_green(" [+] Forward scrape complete", "")
        color_print_green("  ┬  Statistics", "")
        color_print_green(
            "  ├  Forwarded messages found: ", str(obj.forward_count)
        )
        color_print_green(
            "  ├  Forwards from active public chats: ",
            str(obj.forwards_found),
        )
        if hasattr(object, "private_count"):
            color_print_green(
                "  ├  Forwards from private (or now private) chats: ",
                str(obj.private_count),
            )
        color_print_green(
            "  ├  Unique forward sources: ", str(obj.unique_forwards)
        )
        color_print_green(
            "  ├  Top forward source 1: ", str(obj.forward_one)
        )
        color_print_green(
            "  ├  Top forward source 2: ", str(obj.forward_two)
        )
        color_print_green(
            "  ├  Top forward source 3: ", str(obj.forward_three)
        )
        color_print_green(
            "  ├  Top forward source 4: ", str(obj.forward_four)
        )
        color_print_green(
            "  ├  Top forward source 5: ", str(obj.forward_five)
        )
        color_print_green("  └  Edgelist saved to: ", obj.edgelist_file)