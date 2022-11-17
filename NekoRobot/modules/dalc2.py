import pymongo
import asyncio
import random
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

# def commandupdate(update: Update, context: CallbackContext):
#     message = update.effective_message
#     message.reply_text("Hie I have updated my commands\n ❍ /wallet : To View Your Dalcs \n ❍ /topwallets : View Top Users \n ❍ /xbet : Test Your Luck /bet <amount> <heads or tails> \n ❍ /gift : /gift <amount> reply to user \n ❍ `/battle` : Reply to Someone To battle with them")

def dalchelp(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("This Bot has a Currency System Based on spy x family Theme. The Currency is Dalc [Đ] Its just like real money.\nMore Commands will be added soon!\nMeanwhile Heres The Help For Currency System:-\n Currency System Dalc(Đ) \n ❍ /wallet : To View Your Dalcs \n ❍ /topwallets or /top : View Top Users \n ❍ /xbet or /gamble or /b : Test Your Luck /xbet <amount> <heads or tails> \n ❍ /gift or /pay or /donate: /gift <amount> reply to user \n ❍ `/battle` : Reply to Someone To battle with them \n ❍ Reply message with (+, +100) to add dalcs to there Wallet. \n ❍ Reply message with (-, -100) to snitch dalcs from there Wallet.")
  
def gift(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    try:
        # len(message.text) < 2
        # x = len(message.text)
        x = int(message.text.split(' ')[1])
       # return message.reply_text("/gift Enter a Value Noob")
    except IndexError:
        message.reply_text("/gift Enter a Value Noob")
    
    if not message.reply_to_message :
       return message.reply_text("Baka Reply to someone")
    elif message.reply_to_message.from_user.id == message.from_user.id:
        return
    # message.reply_text("Sorry, Anya's Developer is currently working on Gift thing, will complete soon!")
    bot, args = context.bot, context.args
    # message = update.effective_message
    # user_id1 = extract_user(update.effective_message, args)
    user2 = message.from_user
    # user1 = bot.get_chat(user_id1)
    user1 = message.reply_to_message.from_user
    amount = int(message.text.split(' ')[1])
    # user_mention1 = message.reply_to_message.from_user.mention
    # user_mention2 = message.from_user.mention
    # print(user_mention1)
    # print(user_mention2)
    if not is_dalc(user1.id):
      dalc_create(user1.id)
    if not is_dalc(user2.id):
      dalc_create(user2.id)
    
    user1name = app.get_users(int(user1.id))
    user2name = app.get_users(int(user2.id))
    olddalcuser2 = int(mywallet(user2.id))

    if amount > olddalcuser2:
            message.reply_text("Gift Something which you can afford")
    else:
        bot.send_chat_action(chat_id, action="typing")
        olddalcuser1 = int(mywallet(user1.id))
        newdalcuser1 = olddalcuser1 + amount
        collection.update_one({"user_id":f"{user1.id}"}, {'$set':{'dalc': newdalcuser1}})

        newdalcuser2 = olddalcuser2 - amount
        collection.update_one({"user_id":f"{user2.id}"}, {'$set':{'dalc': newdalcuser2}})

        message.reply_text(f"Waku Waku! {user2name.first_name} gifted {amount} dalcs to {user1name.first_name}")
    

# same. random choice from 0 and 1.  (0 loss and 1 win)
# get a random sum of bounty from the fighter. 
# if loss, add the bounty to the victim. (take from fighter)
# if won, get random sum of bounty from the victim and add that to the fighter. (take from victim)


def battle(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot, args = context.bot, context.args
    winlose = int(random.choice(['1','0']))
  
    bot.send_chat_action(chat_id, action="typing")
  
    if not message.reply_to_message :
       return message.reply_text("Baka Reply to someone to Battle")
      
    user1 =  message.reply_to_message.from_user
    user2 = message.from_user
    olddalcuser2 = int(mywallet(user2.id))
    olddalcuser1 = int(mywallet(user1.id))
    user1name = app.get_users(int(user1.id))

      
    if olddalcuser1 > olddalcuser2:
        dalclimit = olddalcuser2
        battleamount = int(random.randrange(0 , dalclimit))

    elif olddalcuser1 < olddalcuser2 :
        dalclimit = olddalcuser1
        battleamount = int(random.randrange(0, dalclimit))

    if not is_dalc(user1.id):
        dalc_create(user1.id)
    if not is_dalc(user2.id):
        dalc_create(user2.id)
      
    if winlose == 1:
        #user2 wins
        newuserdalc2 = olddalcuser2 + battleamount
        collection.update_one({"user_id":f"{user2.id}"}, {'$set':{'dalc': newuserdalc2}})
      
        newuserdalc1 = olddalcuser1 - battleamount
        collection.update_one({"user_id":f"{user1.id}"}, {'$set':{'dalc': newuserdalc1}})
        # bot.send_chat_action(chat_id, action="typing")
        message.reply_text(f"OwO you won! Robbed {battleamount} Đ from {user1name.first_name} ")

    else :
      #user1 wins
        newuserdalc2 = olddalcuser2 - battleamount
        collection.update_one({"user_id":f"{user2.id}"}, {'$set':{'dalc': newuserdalc2}})
        newuserdalc1 = olddalcuser1 + battleamount
        collection.update_one({"user_id":f"{user1.id}"}, {'$set':{'dalc': newuserdalc1}})
        # bot.send_chat_action(chat_id, action="typing")
        message.reply_text(f"Lmao you lost! Gave {battleamount} Đ to {user1name.first_name} from Your Wallet ")

    
      
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
    # bot, args = context.bot, context.args
    message = update.effective_message
    print(message.text)
    # user_id = extract_user(update.effective_message, args)
    # if user_id:
    #   user = bot.get_chat(user_id)
      
    # elif not message.reply_to_message and args:
    #   user = message.from_user
    if message.reply_to_message:
      user_idd = message.reply_to_message.from_user
      count = message.text.split(' ')[1]
    # elif not message.reply_to_message and not args:
    #   user = message.from_user
    else :
      user_idd = message.text.split(' ')[1]
      count = message.text.split(' ')[2]
    # dalcset = int(query)
    
    if not is_dalc(user_idd):
        dalc_create(user_idd)
    try :
        olddalc = int(mywallet(user_idd))
        newdalc = int(count)
    except ValueError:
       message.reply_text("Baka Enter A Valid Value")
    collection.update_one({"user_id":f"{user_idd}"}, {'$set':{'dalc': newdalc}})
    message.reply_text("Updated!")



def bet(update: Update, context: CallbackContext):
    message = update.effective_message
    bot, args = context.bot, context.args
    try :
        u = message.text.split(' ')[2]
    except IndexError:
        message.reply_text("/xbet <value> <heads or tails>")
    # message = update.effective_message
    # user_id = extract_user(update.effective_message, args)
    # message = f"/bet {amount} {choice}"
  
    # if user_id:
    #     user = bot.get_chat(user_id)
    # else :
    
    user = message.from_user
    # m = message.reply_text("Trying Luck...")
    # if userchoice != "heads" or userchoice != "tails":
    #     print("invalid choice")
    
    userchoice = message.text.split(' ')[-1]
    amount = int(message.text.split(' ')[1])
    # print(userchoice)
    # usrchoice = None
    if userchoice == "h" :
        usrchoice = "heads"
    elif userchoice == "t":
        usrchoice = "tails"
    else :
        usrchoice = userchoice
    # print(int(amount))
    choice = random.choice(['heads', 'tails'])

    if not is_dalc(user.id):
        dalc_create(user.id)
   
    if usrchoice.lower() == choice:
        olddalc = int(mywallet(user.id))
        if amount > olddalc:
            message.reply_text("Bet Something which you can afford")
        else :
            newdalc = olddalc + amount
            collection.update_one({"user_id":f"{user.id}"}, {'$set':{'dalc': newdalc}})
            message.reply_text(f"You Won! Added {amount} to your wallet.")
        # print('u won.')
      
    else:
        olddalc = int(mywallet(user.id))
        if amount > olddalc:
            message.reply_text("Bet Something which you can afford")
        else :
            newdalc = olddalc - amount
            collection.update_one({"user_id":f"{user.id}"}, {'$set':{'dalc': newdalc}})
            message.reply_text(f"You Lost :( Took {amount} from your wallet.")
        # print('u lost')



@app.on_message(filters.command(["topwallets", "top"]))
async def top(_, message):
    m = await message.reply_text("Matte! Anya will ask chichi for wallet...")
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
    # print(reversetoplist)
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
        numb = limit + 1
        username = user.username
        msg += f"{numb}. {('@' + username) if username else user_idd} - {dalc_count} Đ\n "
        # msg += f"{limit}. {dalc_count} Đ --> {('@' + username) if username else user_idd}\n"
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
SETGIFT_HANDLER = CommandHandler(["gift", "pay", "donate", "p"], gift , run_async = True)
SETDALC_HANDLER = CommandHandler("setdalc", set_dalc, run_async=True)
MYDALC_HANDLER = CommandHandler(["wallet", "dalc"], mydalcs ,run_async = True)
BET_HANDLER = CommandHandler(["xbet", "b", "gamble"], bet , run_async = True)
# COMMANDUPDATE_HANDLER = CommandHandler(["dalc", "bet", "top"], commandupdate , run_async = True)
DALCHELP_HANDLER = CommandHandler("dalchelp" , dalchelp , run_async = True)
BATTLE_HANDLER = CommandHandler(["battle", "kill", "rob"] , battle , run_async = True)

NEKO_PTB.add_handler(SETDALC_HANDLER)
NEKO_PTB.add_handler(MYDALC_HANDLER)
NEKO_PTB.add_handler(BET_HANDLER)
NEKO_PTB.add_handler(SETGIFT_HANDLER)
# NEKO_PTB.add_handler(COMMANDUPDATE_HANDLER)
NEKO_PTB.add_handler(DALCHELP_HANDLER)
NEKO_PTB.add_handler(BATTLE_HANDLER)


__mod_name__ = "Currency System"
__help__ = """
Currency System Dalc(Đ)
 ❍ `/wallet` or `/dalc` : To View Your Dalcs
 
 ❍ `/topwallets` or `top` : View Top Users
 
 ❍ `/xbet` or `/gamble` or `/b` : Test Your Luck /xbet <amount> <heads or tails> 
 (Fun fact : You can use 'h' or 't' instead of heads or tails too!)
 
 ❍ `/gift` or `pay` or `p` or `donate` : /gift <amount> reply to user
 
 ❍ `/dalchelp` : Get info about this System.
 
 ❍ `/battle` or `/rob` or `/kill`: Reply to Someone To battle with them
 
 ❍ `/setdalc` : /setdalc <userid> <count> (ONLY FOR DEVS)
 
 ❍ Reply message with (`+, +100`) to add dalcs to there Wallet.
 ❍ Reply message with (`-, -100`) to snitch dalcs from there Wallet.
"""

