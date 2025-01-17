# Ported from other Telegram UserBots for SPARKZZZ BOT
# Kangers, don't remove this line 
# @its_vishnu175

from math import ceil
import asyncio
import json
import random
import re
from telethon import events, errors, custom, Button
from userbot import CMD_LIST
import io
from . import telealive

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if query.startswith(
                "**Welcome") and event.query.user_id == bot.uid:
            buttons = [
                (custom.Button.inline(
                    "Stats", data="telestatus"), Button.url(
                    "Source", "https://github.com/vishnu175/SPARKZZZ"))]
            result = builder.article(
                title="SPARKZZZ BOT",
                text=query,
                buttons=buttons
            )
            await event.answer([result] if result else None)
        elif event.query.user_id == bot.uid and query.startswith("`Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            result = builder.article(
                "© SPARKZZZ Help",
                text="{}\nCurrently Loaded Plugins: {}".format(
                    query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False
            )
            await event.answer([result] if result else None)
    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_next\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot from @TeleBotHelp , and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit("Help Menu Closed.")
        else:
            reply_pop_up_alert = "Please get your own userbot from @sparkzzzbotsupport "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_prev\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1,
                CMD_LIST,  # pylint:disable=E0602
                "helpme"
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot from @sparkzzzbotsupport"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"us_plugin_(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = ""
        try:
            for i in CMD_LIST[plugin_name]:
                help_string += i
                help_string += "\n"
        except:
            pass
        if help_string == "":
            reply_pop_up_alert = "{} is useless".format(plugin_name)
        else:
            reply_pop_up_alert = help_string
        reply_pop_up_alert += "\n Use .unload {} to remove this plugin\n\
            © Userbot".format(plugin_name)
        try:
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        except:
            with io.BytesIO(str.encode(reply_pop_up_alert)) as out_file:
                out_file.name = "{}.txt".format(plugin_name)
                await bot.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=plugin_name
                )
    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"telestatus")))
    async def on_plug_in_callback_query_handler(event):
        statustext = await telealive()
        reply_pop_up_alert = statustext
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = 10
    number_of_cols = 3
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [custom.Button.inline(
        "{} {} {}".format(Config.INLINE_EMOJI, x,Config.INLINE_EMOJI),
        data="us_plugin_{}".format(x))
        for x in helpable_plugins]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols], modules[2::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[modulo_page * number_of_rows:number_of_rows * (modulo_page + 1)] + \
            [
            (custom.Button.inline("👈Previous", data="{}_prev({})".format(prefix, modulo_page)),
             custom.Button.inline("⚡Close⚡", data="close"),
             custom.Button.inline("Next👉", data="{}_next({})".format(prefix, modulo_page)))
        ]
    return pairs

             
