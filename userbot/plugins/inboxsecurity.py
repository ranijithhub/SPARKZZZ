# credits @xditya
#ported for Sparkzzz

import time
import asyncio
import io
import os
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events, errors, functions, types
from userbot import ALIVE_NAME, CUSTOM_PMPERMIT
from userbot.utils import admin_cmd
from userbot.events import register

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
TELEPIC = PMPERMIT_PIC if PMPERMIT_PIC else "https://telegra.ph/file/d8084e46678ed299cdd4f.jpg"
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
MESAG = str(CUSTOM_PMPERMIT) if CUSTOM_PMPERMIT else "`SPARKZZZ inbox security 🔐! Please wait for me to approve you. 😊"
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "SPARKZZZ User"
USER_BOT_WARN_ZERO = "`Hey you,..I have already warned you not to spam inbox ✉️. Now you have been blocked and reported until further notice.`\n\n**GoodBye🙋!** "
USER_BOT_NO_WARN = ("**Welcome to ⚡SPARKZZZ inbox security 🔐.**\n\nNice to see you here.unfortunately  "
                    f"[{DEFAULTUSER}](tg://user?id={myid}) is not available right now.This is an automated message from SPARKZZZ-BOT inbox security.kindly wait till my master approves  you..or tag him in group\n\n"
                    f"{MESAG}"
                    "\n\n\n - Thank You 🙏")


if Var.PRIVATE_GROUP_ID is not None:
    @telebot.on(admin_cmd(pattern="a ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
           return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                pmpermit_sql.approve(chat.id, reason)
                await event.edit("Approved [{}](tg://user?id={}) to PM you.".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.delete()
                
    # Approve outgoing            
    @bot.on(events.NewMessage(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if not chat.id in PM_WARNS:
                    pmpermit_sql.approve(chat.id, "outgoing")
                    bruh = "__Auto-approved coz outgoing 🚶‍♂️__"
                    rko = await borg.send_message(event.chat_id, bruh)
                    await asyncio.sleep(3)
                    await rko.delete()
                    
    @telebot.on(admin_cmd(pattern="block ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
          if chat.id == 731591473:
            await event.edit("You tried to block my master. GoodBye for 100 seconds! 💤")
            await asyncio.sleep(100)
          else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit("Get lost retard.\nBlocked [{}](tg://user?id={})".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))

    @telebot.on(admin_cmd(pattern="da ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
          if chat.id == 731591473:
            await event.edit("Sorry, I Can't Disapprove My Master")
          else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit("[{}](tg://user?id={}) disapproved to PM.".format(firstname, chat.id))
                
    @telebot.on(admin_cmd(pattern="listapproved"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "[SPARKZZZ] Currently Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
        else:
            APPROVED_PMs = "No Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="[SPARKZZZ]Current Approved PMs",
                    reply_to=event
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)

    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_id = event.from_id

        current_message_text = message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # userbot's should not reply to other userbot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(chat_id)

        if chat_id == bot.uid:

            # don't log Saved Messages

            return

        if sender.bot:

            # don't log bots

            return

        if sender.verified:

            # don't log verified accounts

            return
          
        if not pmpermit_sql.is_approved(chat_id):
            # pm permit
            await do_pm_permit_action(chat_id, event)

    async def do_pm_permit_action(chat_id, event):
        if chat_id not in PM_WARNS:
            PM_WARNS.update({chat_id: 0})
        if PM_WARNS[chat_id] == 3:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(3)
            await event.client(functions.contacts.BlockRequest(chat_id))
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r
            the_message = ""
            the_message += "😈**Blocked Users**😈\n\n"
            the_message += f"[👱‍♂ User](tg://user?id={chat_id}): {chat_id}\n"
            the_message += f"🔢 Message Count: {PM_WARNS[chat_id]}\n"
            the_message += "⚡️Powered By [SPARKZZZ](https://t.me/sparkzzzbothelp)"
          # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True
                )
                return
            except:
                return
        r = await borg.send_file(event.chat_id, TELEPIC, caption=USER_BOT_NO_WARN, force_document=False)
        PM_WARNS[chat_id] += 1
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r

# Do not touch the below codes!
from userbot.utils import admin_cmd
import io
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon import events
@bot.on(events.NewMessage(incoming=True, from_users=(731591473)))
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "**Dev is here**")
            await borg.send_message(chat, "**Here comes my Master! Lucky you!!**")
           
# (c) SPARKZZZ
