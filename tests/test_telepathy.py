import pytest
from src.telepathy.telepathy import Group_Chat_Analisys, Telepathy_cli
import asyncio


@pytest.fixture
def detail_to_group_basic():
    return {
        "target": "@test15",
        "comprehensive": False,
        "media": False,
        "forwards": False,
        "user": False,
        "export": False,
        "bot": None,
        "location": None,
        "alt": None,
        "json": False,
        "replies": False,
        "translate": False,
        "triangulate_membership": False,
    }

def test_channel_group_basic(detail_to_group_basic):
    tele_cli = Telepathy_cli(
        detail_to_group_basic["target"],
        detail_to_group_basic["comprehensive"],
        detail_to_group_basic["media"],
        detail_to_group_basic["forwards"],
        detail_to_group_basic["user"],
        detail_to_group_basic["bot"],
        detail_to_group_basic["location"],
        detail_to_group_basic["alt"],
        detail_to_group_basic["json"],
        detail_to_group_basic["export"],
        detail_to_group_basic["replies"],
        detail_to_group_basic["translate"],
        detail_to_group_basic["triangulate_membership"],
    )
    group_chan = Group_Chat_Analisys(
        target=detail_to_group_basic["target"],
        client=tele_cli.client,
        log_file=tele_cli.log_file,
        filetime=tele_cli.filetime,
        replies=tele_cli.reply_analysis,
        forwards=tele_cli.forwards_check,
        comprehensive=tele_cli.comp_check,
        media=tele_cli.media_archive,
        json=tele_cli.json_check,
        translate=tele_cli.translate_check,
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tele_cli.client.connect())
    loop.run_until_complete(group_chan.retrieve_self_history(None))
    assert group_chan.history_count > 0
