import json
import requests
from bs4 import BeautifulSoup


x = ""


class infoch():
    def __init__(self, username):
        self.username = username
        url = f"https://t.me/s/{self.username}"
        self.data = requests.get(url).text

    def subs(self):
        data = self.data.split('<div class="tgme_header_counter">')
        data0 = data[-1].split('</div>')[0].replace(" subscribers", "")
        data = data0
        try:
            if 'K' in data0:
                data =  float(data0.replace('K', '')) * 1000
            elif 'M' in data0:
                data =  float(data0.replace('M', '')) * 1000000
            elif 'B' in data0:
                data =  float(data0.replace('B', '')) * 1000000000
            return [float(data),data0]
        except:
            return "no post"

    def vpm(self):
        data = self.data.split('<span class="tgme_widget_message_views">')
        data0 = data[-1].split('</span>')[0]
        data = data0
        try:
            if 'K' in data0:
                data =  float(data0.replace('K', '')) * 1000
            elif 'M' in data0:
                data =  float(data0.replace('M', '')) * 1000000
            elif 'B' in data0:
                data =  float(data0.replace('B', '')) * 1000000000
            return [float(data), data0]
        except:
            return "no post"

    def name(self):
        data = self.data.split('<title>')
        data = data[-1].split('Telegram')[0]
        return data
    
    def idx(self):
        url = f"https://api.telegram.org/bot{x}/getChat?chat_id=@{self.username}"
        data = requests.get(url).text
        data = json.loads(data)
        id = data.get("result").get("id")
        return id
    
    def admin(self):
        url = f"https://api.telegram.org/bot{x}/getChatAdministrators?chat_id=@{self.username}"
        data = requests.get(url).text
        data = json.loads(data)
        return data.get("ok")
    
    def latestpost(self):
        url = f"https://t.me/s/{self.username}"
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'lxml')
        text = soup.prettify()
        id = ('<div class="tgme_widget_message'+
        ' text_not_supported_wrap js-widget_message" data-post="')
        text = text.split(id)[-1]
        id = '" data-view'
        text = text.split(id)[0].split("/")[-1]
        print(text)



