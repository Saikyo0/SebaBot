from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
import ast
import pay
from tools import infoch
from datetime import date

Token = ""
SERVICEACCOUNT = ""

class bot:
    def __init__(self) -> None:
        self.state = ""
        self.user_info = {}
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = './credentials.json' 
        credentials = service_account.Credentials.from_service_account_file(
                   SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_creds = credentials.with_subject('')
        self.service = build('drive', 'v3', credentials=delegated_creds)
        self.goldchannels = []
        self.silverchannels = []
        self.bronzechannels = []
        self.ch_id = ""
    
    def getchannels(self):
        results = self.service.files().list(q = "'' in parents", pageSize=10,fields="files(id, name)").execute()
        items = results.get('files', [])
        file_id = ""
        for item in items:
            if item["name"] == "channelslist.txt":
                file_id = item["id"]
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        file = ast.literal_eval(fh.getvalue().decode("utf-8") )
        if "gold" in file.keys():
            self.goldchannels = file["gold"]
        if "silver" in file.keys():
            self.silverchannels = file["silver"]
        if "bronze" in file.keys():
            self.bronzechannels = file["bronze"]
        self.vnum = 0

    def start(self, update: Update, context: CallbackContext) -> None:
        self.state = ""
        self.user_info = {}
        self.user = str(update.message.from_user.id)
        results = self.service.files().list(q = "'1QN89_KtfNm3eKzc84Tms2Lm74issdcIp' in parents", pageSize=10,fields="files(id, name)").execute()
        items = results.get('files', [])
        file_id = ""
        exists = False
        for item in items:
            if item["name"] == f"{self.user}.txt":
                file_id = item["id"]
                exists = True
            if item["name"] == "channelslist.txt":
                self.ch_ids = item["id"]
        if exists:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            file = fh.getvalue().decode("utf-8")
            self.user_info = ast.literal_eval(file)
        else:
            usrfile = open(f"{self.user}.txt", "w+")
            text = "{'Language': 'Amharic', 'Tokens': '0', 'Time': '" +   str(date.today()) + "'}"
            usrfile.write(text)
            usrfile.close()
            media = MediaFileUpload(f'{self.user}.txt', mimetype='text/plain',resumable=True)
            request = self.service.files().create(media_body=media,
                body={'name': f'{self.user}.txt', 'parents': ['1QN89_KtfNm3eKzc84Tms2Lm74issdcIp']} )
            response = None
            while response is None:
                    status, response = request.next_chunk()
            self.user_info = ast.literal_eval(text)
            update.message.reply_text("Account Creation Complete!")

        if self.user_info['Language']=='Amharic':
            keyboard = [[InlineKeyboardButton('📺 ቻናል Megzat', callback_data="buychannels")],
                        [InlineKeyboardButton('💰 ቻናል meshet', callback_data="sellchannel")],
                        [InlineKeyboardButton('📒 የእኔ ሒሳብ', callback_data="account")],
                        [InlineKeyboardButton('🙋 እገዛ', callback_data="help"),
                        InlineKeyboardButton('⚙️ ቅንብሮች', callback_data="settings")]]
            text=f"ሰላም {update.message.from_user.first_name} \n  _______ ______ _____ ___, አጠቃላይ ሂደቱን ለመረዳት 'እገዛ' የሚለው Button ይንኩት"
            update.message.reply_text(text,reply_markup=(InlineKeyboardMarkup(keyboard)))

        if self.user_info['Language']=='English':
            keyboard = [[InlineKeyboardButton('📺 BUY CHANNEL', callback_data="buychannels")],
                        [InlineKeyboardButton('💰 SELL CHANNELS', callback_data="sellchannel")],
                        [InlineKeyboardButton('📒 MY ACCOUNT', callback_data="account")],
                        [InlineKeyboardButton('🙋 HELP', callback_data="help"),
                        InlineKeyboardButton('⚙️ SETTINGS', callback_data="settings")]]
            text=f"Hi {update.message.from_user.first_name} \n  ___________ _____ ___, To Understand The Whole Process Click On The 'HELP' Below"
            update.message.reply_text(text,reply_markup=(InlineKeyboardMarkup(keyboard))) 

    def goldkeyboard(self, update, context, num) -> None:
        keyboard = [[]]
        x = -1
        y = -1
        for channel in self.goldchannels:
            if channel != []:
                channel = list(channel.keys())[0]
                info = infoch(channel)
                name = info.name()
                subs = info.subs()
                if subs != "no post":
                    if x%3 == 0:
                        x += 1
                        keyboard[y].append(InlineKeyboardButton(f"Next", callback_data=f"nextgold"))
                        y += 1
                    keyboard[y].append(InlineKeyboardButton(f"{name} {subs[-1]} subs",
                        callback_data=f"fbuy_{channel}"))
        return [keyboard[num]]

    def silverkeyboard(self, update, context, num) -> None:
        keyboard = [[]]
        x = -1
        y = -1
        for channel in self.silverchannels:
            if channel != []:
                channel = list(channel.keys())[0]
                info = infoch(channel)
                name = info.name()
                subs = info.subs()
                if subs != "no post":
                    if x%10 == 0:
                        x += 1
                        keyboard[y].append(InlineKeyboardButton(f"Next", callback_data=f"nextsilver"))
                        y += 1
                    keyboard[y].append(InlineKeyboardButton(f"{name} {subs[-1]} subs",
                        callback_data=f"fbuy_{channel}"))
        return [keyboard[num]]

    def bronzekeyboard(self, update, context, num) -> None:
        keyboard = [[]]
        x = -1
        y = -1
        for channel in self.bronzechannels:
            if channel != []:
                channel = list(channel.keys())[0]
                info = infoch(channel)
                name = info.name()
                subs = info.subs()
                if subs != "no post":
                    if x%10 == 0:
                        x += 1
                        keyboard[y].append(InlineKeyboardButton(f"Next", callback_data=f"nextbronze"))
                        y += 1
                    keyboard[y].append(InlineKeyboardButton(f"{name} {subs[-1]} subs",
                        callback_data=f"fbuy_{channel}"))
        return [keyboard[num]]
    
    def controller(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        if query.data == "menu":
            if self.user_info['Language']=="Amharic":
                keyboard = [[InlineKeyboardButton('📺 ቻናል መግዛት', callback_data="buychannels")],
                            [InlineKeyboardButton('💰 ቻናል መሸጥ', callback_data="sellchannel")],
                            [InlineKeyboardButton('📒 የእኔ ሒሳብ', callback_data="account")],
                            [InlineKeyboardButton('🙋 እርዳታ', callback_data="help"),
                            InlineKeyboardButton('⚙️ ቅንብሮች', callback_data="settings")]]
                text=f"ሰላም {query.message.from_user.first_name} \n  _______ ______ _____ ___, አጠቃላይ ሂደቱን ለመረዳት 'እገዛ' የሚለው Button ይንኩት"
                query.message.edit_text(text,reply_markup=(InlineKeyboardMarkup(keyboard)))
            if self.user_info['Language']=="English":
                keyboard = [[InlineKeyboardButton('📺 BUY CHANNEL', callback_data="buychannels")],
                            [InlineKeyboardButton('💰 SELL CHANNEL', callback_data="sellchannel")],
                            [InlineKeyboardButton('📒 MY ACCOUNT', callback_data="account")],
                            [InlineKeyboardButton('🙋 HELP', callback_data="help"),
                            InlineKeyboardButton('⚙️ SETTINGS', callback_data="settings")]]
                text=f"Hi {query.message.from_user.first_name} \n  ___________ _____ ___, To Understand The Whole Process Click On The 'HELP' Below"
                query.message.edit_text(text,reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif str(query.data).startswith("Language"):
            if str(query.data).endswith('en'):
                keyboard = [[InlineKeyboardButton('Account Info', callback_data="change_info")],
                            [InlineKeyboardButton('History', callback_data="history")],
                            [InlineKeyboardButton('ቋንቋ', callback_data="language_am")],
                            [InlineKeyboardButton('Menu', callback_data="menu")]]
                query.message.edit_text(text="Settings:",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
            else:
                keyboard = [[InlineKeyboardButton('ሂሳብ መረጃ', callback_data="change_info")],
                            [InlineKeyboardButton('ታሪክ', callback_data="history")],
                            [InlineKeyboardButton('ቋንቋ', callback_data="language_en")],
                            [InlineKeyboardButton('ተመለስ', callback_data="menu")]]

                query.message.edit_text(text="ቅንብሮች: ",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif query.data == "buychannels":
            self.getchannels()
            if self.user_info['Language']=="Amharic":
                keyboard = [[InlineKeyboardButton('Gold (በሰዓት 15ሺህ views)', callback_data="buygold")],
                            [InlineKeyboardButton('Silver (በሰዓት 10ሺህ views)', callback_data="buysilver")],
                            [InlineKeyboardButton('Bronze (በሰዓት 5k views)', callback_data="buybronze")]]
                query.message.edit_text(text="Choose Package: ",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
            if self.user_info['Language']=="English":
                keyboard = [[InlineKeyboardButton('Gold (15k views per hour)', callback_data="buygold")],
                            [InlineKeyboardButton('Silver (10k  views per hour)', callback_data="buysilver")],
                            [InlineKeyboardButton('Bronze (5k views per hour)', callback_data="buybronze")]]
                query.message.edit_text(text="Choose Package: ",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif query.data == "buygold":
            self.vnum = 0
            keyboard = self.goldkeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ",
                                    reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif  query.data == "nextgold":
            self.vnum += 1
            keyboard = self.goldkeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ", reply_markup=(keyboard))
        elif query.data == "buysilver":
            self.vnum = 0
            keyboard = self.silverkeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ",
                                    reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif  query.data == "nextsilver":
            self.vnum += 1
            keyboard = self.silverkeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ", reply_markup=(keyboard))
        elif query.data == "buybronze":
            self.vnum = 0
            keyboard = self.bronzekeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ",
                                    reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif  query.data == "nextbronze":
            self.vnum += 1
            keyboard = self.bronzekeyboard(query, CallbackContext, self.vnum)
            query.message.edit_text(text="Choose : ", reply_markup=(keyboard))
        elif query.data.startswith('fbuy_'):
            username = query.data.replace("fbuy_","")
            channel = infoch(username)
            views = channel.vpm()[-1]
            subs = channel.subs()[-1]
            names = channel.name()
            if subs != "no post" and views != "no post":
                if self.user_info['Language']=="English":
                    text = f"{names} \n SUBS: {subs} \n VIEWS: {views}"
                    keyboard = [[InlineKeyboardButton("Confirm", callback_data=f"dbuy_{username}")],
                                [InlineKeyboardButton("Cancel", callback_data=f"dbuy_{username}")]]
                    query.message.edit_text(text=text,
                                            reply_markup=(InlineKeyboardMarkup(keyboard)))
                if self.user_info['Language']=="Amharic":
                    text = f"{names} \n SUBS: {subs} \n VIEWS: {views}"
                    keyboard = [[InlineKeyboardButton("Confirm", callback_data=f"dbuy_{username}")],
                                [InlineKeyboardButton("Cancel", callback_data=f"dbuy_{username}")]]
                    query.message.edit_text(text=text,
                                            reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif query.data.startswith('dbuy_'):
            query.message.edit_text(text="Send Channel You'll promote: ")
            username = query.data.replace("dbuy_","")
            self.state = f"approval{username}"
        elif query.data.startswith('apv'):
            if query.data.endswith("&"):
                ids = (query.data.replace("apv_","").replace("&","")).split(",")
                buyerid = int(ids[-1])
                channelid = ids[0]
                moon = infoch(channelid).idx()
                self.state = f"ad{moon}"
                self.user_info = {}
                self.user = str(update.message.from_user.id)
                results = self.service.files().list(q = "'1QN89_KtfNm3eKzc84Tms2Lm74issdcIp' in parents", pageSize=10,fields="files(id, name)").execute()
                items = results.get('files', [])
                file_id = ""
                for item in items:
                    if item["name"] == f"{self.user}.txt":
                        file_id = item["id"]
                request = self.service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                file = fh.getvalue().decode("utf-8")
                self.user_info = ast.literal_eval(file)
                if channelid in self.goldchannels:
                    self.user_info["Tokens"] =str(int(self.user_info["Tokens"]) - 10)
                if channelid in self.bronzechannels:
                    self.user_info["Tokens"] =str(int(self.user_info["Tokens"]) - 100)
                if channelid in self.silverchannels:
                    self.user_info["Tokens"] =str(int(self.user_info["Tokens"]) - 1000)
                
                query.bot.send_message(buyerid,f"Your ad on: @{channelid} has been approved!\n"+
                                                "Please send the ad to be posted on the channel")

            elif query.data.endswith("#"):
                ids = (query.data.replace("apv_","").replace("#","")).split(",")
                ownerid = int(ids[-1])
            if self.user_info['Language']=="English":
                query.bot.send_message(ownerid,f"Your ad on: @{ids[0]} has been denied.")
            if self.user_info['Language']=="Amharic":
                query.bot.send_message(ownerid,f"በ @{ids[0]} ላይ የተጠየቀው ማስታወቂያ ታግዷል")
        elif query.data == "sellchannel":
            self.state = "sellchannels"
            if self.user_info['Language']=="Amharic":
                query.message.reply_text(text="የእርስዎን ቻናል Username ይላኩ: ")
            elif self.user_info['Language']=="English":
                query.message.reply_text(text="Send Your Channel's Username: ")
        elif query.data == "account":
            if self.user_info['Language']=="Amharic":
                text = (f"ስም: {query.message.from_user.first_name}\n"+
                        f"ቶከኖች: {self.user_info['Tokens']}\n"+
                        f"የተከፈተው በ: {self.user_info['Time']}\n")
                keyboard = [[InlineKeyboardButton('ማስቀመጫ', callback_data="deposit")],
                            [InlineKeyboardButton('ማውጣት', callback_data="withdraw")],
                            [InlineKeyboardButton('Menu', callback_data="menu")]]
                query.message.edit_text(text,
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
            if self.user_info['Language']=="English":
                text = (f"Name: {query.message.from_user.first_name}\n"+
                        f"Tokens: {self.user_info['Tokens']}\n"+
                        f"Created on: {self.user_info['Time']}\n")
                keyboard = [[InlineKeyboardButton('Deposit', callback_data="deposit")],
                            [InlineKeyboardButton('Withdraw', callback_data="withdraw")],
                            [InlineKeyboardButton('Menu', callback_data="menu")]]
                query.message.edit_text(text,
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
        elif query.data == "help":
            if self.user_info['Language']=="Amharic":
                query.message.reply_text(text="FAQ: \n1,Buy Channel: buy ad spots"+
                                                    "\n2, Sell Channel: sell ad spots from your channel"+
                                                    "\n3, Account: Contains your telegram account info and history"+
                                                    "\n4, Settings: options to change language and more in the future")
            if self.user_info['Language']=="English":
                query.message.reply_text(text="FAQ: \n1,Buy Channel: buy ad spots"+
                                                    "\n2, Sell Channel: sell ad spots from your channel"+
                                                    "\n3, Account: Contains your telegram account info and history"+
                                                    "\n4, Settings: options to change language and more in the future")
        elif query.data == "settings":
            if self.user_info['Language']=="Amharic":
                keyboard = [[InlineKeyboardButton('Account መረጃ', callback_data="change_info")],
                            [InlineKeyboardButton('ታሪክ', callback_data="history")],
                            [InlineKeyboardButton('Language', callback_data="language_en")],
                            [InlineKeyboardButton('Menu', callback_data="menu")]]

                query.message.edit_text(text="ቅንብሮች: \n ________\n _______",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
            elif self.user_info['Language']=="English":
                keyboard = [[InlineKeyboardButton('Account Info', callback_data="change_info")],
                            [InlineKeyboardButton('History', callback_data="history")],
                            [InlineKeyboardButton('ቋንቋ', callback_data="language_am")],
                            [InlineKeyboardButton('Menu', callback_data="menu")]]
                query.message.edit_text(text="Settings:",
                                        reply_markup=(InlineKeyboardMarkup(keyboard)))
    
    def messagehandler(self, update: Update, context: CallbackContext) -> None:
        if self.state.startswith("sellchannels"):
            username = update.message.text
            username = (username.replace("@",""))
            uinfo = infoch(username)
            if uinfo.admin():
                ch_id = str(uinfo.idx())
                views = uinfo.vpm()
                subs = uinfo.subs()
                if views != "no post" and subs != "no post":
                    name = uinfo.name()
                    user_name = update.message.from_user.id
                    if views[0] > 10000 and subs[0] > 10000:
                        tier = "gold" 
                    elif views[0] > 1000 and subs[0] > 1000:
                        tier = "silver"
                    else:
                        tier = "bronze"
                    text = {tier: [{username: {"Owner": f"{user_name}","id":ch_id}}]}
                    if tier == "gold":
                        self.goldchannels.append(text[tier][0][username])
                    elif tier == "silver":
                        self.silverchannels.append(text[tier][0][username])
                    else:
                        self.bronzechannels.append(text[tier][0][username])
                    results = self.service.files().list(q = "'1QN89_KtfNm3eKzc84Tms2Lm74issdcIp' in parents", pageSize=10,fields="files(id, name)").execute()
                    items = results.get('files', [])
                    file_id = ""
                    for item in items:
                        if item["name"] == "channelslist.txt":
                            file_id = item["id"]
                    request = self.service.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    text_ = {username: {"Owner": f"{user_name}"}}
                    while done is False:
                        status, done = downloader.next_chunk()
                    if fh.getvalue().decode("utf-8").startswith("{"):
                        text_c = ast.literal_eval(fh.getvalue().decode("utf-8"))
                        if text_ not in text_c[tier]:
                            text = text_c[tier].append(text_)
                            text = str(text_c)
                    else:
                        text = str(text)
                    file = open("channelslist.txt", "w+")
                    file.write(str(text))
                    file.close()
                    file = self.service.files().get(fileId=file_id).execute()
                    media_body = MediaFileUpload(
                        "channelslist.txt", resumable=True)
                    request = self.service.files().update(
                        fileId=file_id,
                        media_body=media_body).execute()
                    update.message.reply_text("Your Channel has been submitted successfully! \n Results:\n"
                                            f"{name} \n TIER: {tier} \n SUBS: {subs[-1]} \n Latest views: {views[-1]}")
                else:
                    update.message.reply_text("No Post!")
            else:
                update.message.reply_text("Bot isnt admin!")
            self.state = ""
        if self.state.startswith("approval"):
            info_id = update.message.text.replace("@","")
            update.message.reply_text("Request Submitted, Waiting for approval")
            usernamex = self.state.replace("approval","")
            ad_id = usernamex
            results = self.service.files().list(q = "'1QN89_KtfNm3eKzc84Tms2Lm74issdcIp' in parents", pageSize=10,fields="files(id, name)").execute()
            items = results.get('files', [])
            file_id = ""
            for item in items:
                if item["name"] == "channelslist.txt":
                    file_id = item["id"]
                    break
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            channels = ast.literal_eval(fh.getvalue().decode("utf-8"))
            ownerid = ""
            for tier in channels:
                for channel_ in channels[tier]:
                    for channel in channel_:
                        if channel == ad_id:
                            ownerid = channel_[ad_id].get("Owner")
                            break
            channelinfo = infoch(info_id)
            name = channelinfo.name()
            subs = channelinfo.subs()
            views = channelinfo.vpm()
            text = ("Following Channel wants to post an ad: \n"
                    f"Name: {name} \nSubs: {subs} \nViews: {views}")
            buyer = update.message.from_user.id
            ids = f"{ad_id},{buyer}"
            keyboard = [[InlineKeyboardButton('Approve', callback_data=f"apv_{ids}&")],
                        [InlineKeyboardButton('Disprove', callback_data=f"apv_{ids}#")]]
            update.message.bot.send_message(chat_id=ownerid,text=text,
                                reply_markup=(InlineKeyboardMarkup(keyboard)))
            self.state = ""
        if self.state.startswith("ad"):
            idx=self.state.replace("ad","")
            uid = int(idx)
            update.message.copy(uid)
            update.message.reply_text("AD sucessfully Posted!!")
            self.state = ""

    def main(self) -> None:
        updater = Updater(Token)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CommandHandler('menu', self.start))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.controller))
        updater.dispatcher.add_handler(MessageHandler(Filters.all, self.messagehandler))
        updater.start_polling()
        updater.idle()


bot().main()
