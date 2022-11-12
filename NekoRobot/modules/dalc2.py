import pymongo
import asyncio
from pyrogram import filters
from NekoRobot import pgram as app
from NekoRobot.utils.filter_groups import karma_negative_group, karma_positive_group
from NekoRobot.mongo import db
from NekoRobot.modules.helper_funcs.extraction import extract_user
from NekoRobot.modules.disable import DisableAbleCommandHandler
from telegram import MessageEntity, Update
from telegram.ext import CallbackContext,Filters,MessageHandler, CommandHandler
import NekoRobot.modules.sql.users_sql as sql
from NekoRobot.modules.helper_funcs.chat_status import sudo_plus
from NekoRobot import NEKO_PTB

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|thanx|thanks|pro|cool|good|pro|pero|op|nice|noice|best|uwu|owo|right|correct|peru|piro|👍|\+100)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|baka|idiot|chutiya|nub|noob|wrong|incorrect|chaprii|chapri|weak|\-100)$"

# connectionString = "mongodb+srv://chirag57:A9325442737a@vanitasxbot.65vdlwk.mongodb.net/?retryWrites=true&w=majority"

# client = pymongo.MongoClient(connectionString)

# db = client['tempdalc']

collection = db.dalc 
# user_id = 12345456
m=1
def last(n):
    return n[m]  
   
# function to sort the tuple   
def sort(tuples):
  
    # We pass used defined function last
    # as a parameter. 
    return sorted(tuples, reverse=True ,key = last, )

def dalc_create(user_id):
    base = {
        "user_id":f"{user_id}",
        "dalc": 100
    }
    create = collection.insert_one(base).inserted_id

def is_dalc(user_id):
    isdalc = collection.find_one({"user_id":f"{user_id}"})
    if isdalc:
        return True
    else :
        return False

def mywallet(user_id):
    dalcs = collection.find_one({"user_id":f"{user_id}"})
    # print(dalcs["dalc"])
    return dalcs["dalc"]

  
def mydalcs(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)
      
    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("I can't Find A wallet")
        return

    else :
      return
    print(user.id)
      
    # user_id = extract_user(update.effective_message, args)
    # user = message.from_user
    if not is_dalc(user.id):
      dalc_create(user.id)
    dalcs = collection.find_one({"user_id":f"{user.id}"})
    mydalc = dalcs["dalc"]
    message.reply_text(f"Current Dalcs = {mydalc} Đ")


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
    if not is_dalc(user_id):
        dalc_create(user_id)
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    user_mention = message.reply_to_message.from_user.mention
    olddalc = int(mywallet(user_id))
    newdalc = olddalc + 100
    collection.update_one({"user_id":f"{user_id}"}, {'$set':{'dalc': newdalc}})
    await message.reply_text(
        f"Waku Waku! Anya added 100 dalcs to {user_mention}'s Wallet\nCurrent Dalcs: {newdalc} Đ"
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
    if not is_dalc(user_id):
        dalc_create(user_id)
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    user_mention = message.reply_to_message.from_user.mention
    olddalc = int(mywallet(user_id))
    newdalc = olddalc - 100
    collection.update_one({"user_id":f"{user_id}"}, {'$set':{'dalc': newdalc}})
    await message.reply_text(
        f"Anya is Sad :( took 100 dalcs from {user_mention}'s Wallet\nCurrent Dalcs: {newdalc} Đ"
    )


@sudo_plus
def set_dalc(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(update.effective_message, args)
    if user_id:
      user = bot.get_chat(user_id)
      
    elif not message.reply_to_message and args:
      user = message.from_user

    # elif not message.reply_to_message and not args:
    #   user = message.from_user
      
    query = message.text.split(None, 1)[1]
    # dalcset = int(query)
    
    # if not is_dalc(user.id):
    #     dalc_create(user.id)
    try :
        olddalc = int(mywallet(user.id))
        newdalc = int(query)
    except ValueError:
       message.reply_text("Baka Enter A Valid Value")
    collection.update_one({"user_id":f"{user.id}"}, {'$set':{'dalc': newdalc}})



@app.on_message(filters.command("top") & filters.group)
async def top(_, message):
    m = await message.reply_text("`Matte! Anya will ask chichi for wallet...`")
    msg = "Top Wallets:- \n"
    limit = 0
    toplist = []
    L = [1,2,3,4,5,6,7,8,9,10]
    tops = collection.find({})
    for topuser in tops:
        # print(topuser["dalc"])
        usernames = topuser["user_id"]
        dalcofusers = topuser["dalc"]
        toplist.append((usernames, dalcofusers))
    reversetoplist = sort(toplist)
    print(reversetoplist)

    for user_idd, dalc_count in reversetoplist:
        # print(user_id)
        # print(dalc_count)
        if limit>9:
            break 
        try:
            user = await app.get_users(int(user_idd))
            await asyncio.sleep(0.8)
        except Exception:
            continue
        first_name = user.first_name
        if not first_name:
            continue
        username = user.username
        msg += f"{dalc_count} --> {('@' + username) if username else user_idd}\n"
        limit += 1 
    await m.edit(msg)
# {(first_name[0.12] + '...') if len(first_name) > 12 else first_name}
    # toplist.sort()
    # for index, element in enumerate(L):
        # reversetoplist.append((index,element))
    # for i in dalc:
 
# upvote()
# dalc_create(12345678)
# hi = is_dalc(user_id)
# print(hi)
# print(return)
# downvote(12345456)
# top()
SETDALC_HANDLER = CommandHandler("setdalc", set_dalc, run_async=True)
MYDALC_HANDLER = CommandHandler("dalc", mydalcs ,run_async = True)

NEKO_PTB.add_handler(SETDALC_HANDLER)
NEKO_PTB.add_handler(MYDALC_HANDLER)

__mod_name__ = "Currency System"
__help__ = """
Currency System[Dalc(Đ)]
 ❍ `/dalc` : To View Your Dalcs
 ❍ `/top` : View Top Users
 ❍ `/setdalc` : Reply to user /setdalc <value> (ONLY FOR DEVS)
 ❍ Reply message with (`+, +100`) to add dalcs to there Wallet.
 ❍ Reply message with (`-, -100`) to snitch dalcs from there Wallet.
"""

