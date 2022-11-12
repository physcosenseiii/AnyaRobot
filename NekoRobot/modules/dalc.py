import asyncio

from pyrogram import filters

import NekoRobot.modules.mongo.dalc_mongo as sql
from NekoRobot.modules.userinfo import get_id
from NekoRobot.modules.helper_funcs.extraction import extract_user
from NekoRobot.modules.disable import(
    DisableAbleCommandHandler,
    DisableAbleMessageHandler
)
from NekoRobot import pgram as app
from telegram.ext import CallbackContext,Filters,MessageHandler
from telegram import MessageEntity, Update
from NekoRobot.ex_plugins.newdbfunctions import(
    alpha_to_int,
    int_to_alpha,
    get_dalcs,
    update_dalc
)

from NekoRobot.pyro.errors import capture_err
from NekoRobot.utils.filter_groups import karma_negative_group, karma_positive_group

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$"

@app.on_message(
  filters.text
  & filters.group
  & filters.incoming
  & filters.reply
  & filters.regex(regex_upvote)
  & ~filters.via_bot
  & ~filters.bot,
  group=karma_positive_group,
)
async def upvote(_,message):
    user_id = message.reply_to_message.from_user.id
    # is_dalc = sql.is_dalc(user_id) 
    # if not is_dalc:
    #     return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    user_mention = message.reply_to_message.from_user.mention
    
    current_dalc = await get_dalcs(user_id)
    if current_dalc:
        current_dalc = current_dalc['dalc']
        dalc = dalc + 100

    else :
        dalc = 100

    new_dalc = {"dalc":dalc}
    await update_dalc(user_id, new_dalc)
    await message.reply_text(
        f"Waku Waku! Anya added 100 dalcs to {user_mention}'s Wallet\nCurrent Dalcs: {dalc} Đ"
    )  

@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,  
)
async def downvote(_,message):
    user_id = message.reply_to_message.from_user.id
    # is_dalc = sql.is_dalc(user_id) 
    # if not is_dalc:
    #     return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    user_mention = message.reply_to_message.from_user.mention
    
    current_dalc = await get_dalcs(user_id)
    if current_dalc:
        current_dalc = current_dalc['dalc']
        dalc = dalc - 100

    else :
        dalc = 100

    new_dalc = {"dalc":dalc}
    await update_dalc(user_id, new_dalc)
    await message.reply_text(
        f"Anya is Sad :( took 100 dalcs from {user_mention}'s Wallet\nCurrent Dalcs: {dalc} Đ"
    )

# @app.on_message(filters.command("topdalc") & filters.group)
# async def dalc(_, message):
#     if not message.reply_to_message:
#         m = await message.reply_text("Matte! Anya will ask chichi for wallet...")

# @app.on_message(filters.command("mywallet") & filters.group)
async def mywallet(update: Update, context: CallbackContext, _,message):
    # user_id = message.
    message = update.effective_message
    bot, args = context.bot, context.args
    user_id = extract_user(update.effective_message, args)
    dalc = await get_dalcs(user_id)
    dalc = dalc["dalc"] if dalc else 0
    await message.reply_text(f"Total Dalcs: {dalc} Đ")

__mod_name__ = "Dalc System"

__help__ = """
Currency System[Dalc(Đ)]
 ❍ `/dalc` : To enable / disable Currency system
 ❍ `/mywallet`: Show your dalcs
 ❍ Reply message with (`+, +100) to add dalcs to there Wallet.
 ❍ Reply message with (`-, -100`) to snitch dalcs from there Wallet.
"""