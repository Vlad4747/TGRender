
from settings import *

from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from pyrogram import *
from  pyrogram.raw.base import UserStatus
import time
from test import *
import textwrap

# делает кружочки из квадратных изображений
def func(im):
    def prepare_mask(size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size,  Image.LANCZOS)


    def crop(im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.LANCZOS)

    size = (200, 200)


    im = crop(im, size)
    im.putalpha(prepare_mask(size, 4))
    return im
# находит самую длиную строчку и её длину
def get_max_width(text):
    lines = text.splitlines()
    maxWidth = 0
    maxLine = ""
    for line in lines:
        if len(line)>maxWidth:
            maxWidth = len(line)
            maxLine = line
    return maxWidth,maxLine

class Render:
    def __init__(self,app):
        self.app = app
        self.n4G = Image.open("4g.png").resize((40,40))
        self.paper_clip = Image.open("1.png").resize((70,70))
        self.display = Image.new('RGB', res, (50,56,67))
        self.draw = ImageDraw.Draw(self.display)
        self.ava = func(Image.open("downloads/ava.png")).resize((50,50))
        self.wallpaper = Image.open("Wallpapers/0.jpg").resize(res)



    def panel(self):
        #
        current_datetime = datetime.now()
        args = str(current_datetime).split(":")
        time = args[0].split()[1] + ":" + args[1]
        self.draw.rectangle((0, 0, width, 30), fill="white")
        myFont = ImageFont.truetype("OpenSans.ttf", size=20)
        print(myFont)
        self.draw.text((10, 5), time, fill="black", font=myFont)
        self.draw.text((width - 45, 5), "78%", fill="black", font=myFont)
        self.display.paste(self.n4G, (width - 80, -4), mask=self.n4G)
    def chat(self):
        #ajy
        self.display.paste(self.wallpaper,(0,0))
        #кордената y соопшения
        y = height - 100
        myFont = ImageFont.truetype("OpenSans.ttf", size=30)
        for m in self.app.client.client.get_chat_history(cusr, limit=30):
            try:
                right = False
                if m.from_user.id == self.app.client.my_id:
                    right = True
                text = textwrap.fill(m.text, maxW)
                m_time = str(m.date).split()[1].split(":")[0]+":"+str(m.date).split()[1].split(":")[1]
                print(text,m_time)
                lines = text.splitlines()
                #
                text_size = myFont.getbbox(get_max_width(text)[1])
                #print(text_size)
                # set button size + 10px margins
                msg_size = (text_size[2] - text_size[0] + 50, text_size[3] + text_size[1] + 40)
                if right:
                    self.draw.rounded_rectangle((width-20-msg_size[0], y - len(lines) * 30 - 20,width-10, y),
                                                fill=(82, 84, 86), radius=16)
                    i = 0
                    for line in lines:
                        self.draw.text((width-10-msg_size[0], y - len(lines) * 30 + i - 18), text=line.rstrip(), fill="white",
                                       font=myFont)
                        i += 30
                    myFont2 = ImageFont.truetype("OpenSans.ttf", size=16)
                    self.draw.text((width-60, y - len(lines) * 30 + i - 30), text=m_time,
                                   fill=(162, 164, 166),
                                   font=myFont2)
                    y -= len(lines) * 30 + 30
                else:
                    self.draw.rounded_rectangle((10, y - len(lines) * 30 - 20, 30 + msg_size[0], y), fill=(82, 84, 86), radius=16)
                    i = 0
                    for line in lines:
                        self.draw.text((20, y - len(lines) * 30 + i - 18), text=line.rstrip(), fill="white", font=myFont)
                        i += 30
                    myFont2 = ImageFont.truetype("OpenSans.ttf", size=16)
                    self.draw.text((msg_size[0]-20, y - len(lines) * 30 + i - 30), text=m_time, fill=(162, 164, 166),
                                   font=myFont2)
                    y -= len(lines) * 30 + 30
            except:
                pass
        # ЭТО прямогольник с назгнаием и икнокой чата
        self.draw.rectangle((0, 30, width, 100), fill=(43, 44, 46))
        myFont = ImageFont.truetype("OpenSans.ttf", size=50)

        # хз как написать сам догодаешься
        self.draw.rectangle((0, height - 80, width, height), fill=(42, 44, 46))
        self.draw.text((80, height - 70), text="Cообщение", fill=(62, 64, 66), font=myFont)

        # скрепка рисуется
        self.display.paste(self.paper_clip, (2, height - 70), mask=self.paper_clip)
        # аватарка
        self.display.paste(self.ava, (10, 40), mask=self.ava)
        # Имя
        myFont = ImageFont.truetype("OpenSans.ttf", size=30)
        self.draw.text((70, 40), text=self.app.client.name, fill="white", font=myFont)
    def save(self):
        self.display.save("screen.png")
class ClientTG:
    def  __init__(self,app):
        self.app = app
        self.client = Client('name', api_id, api_hash)
        self.client.start()
        self.chat = self.client.get_chat(cusr)
        self.my_id = self.client.get_me().id
        self.name = self.chat.first_name
        if self.chat.last_name:
            self.name += ' ' + self.chat.last_name
        photo_file_id = self.chat.photo.small_file_id
        self.client.download_media(photo_file_id,"ava.png")
        #со статусом не разобрался
        g = self.client.get_users(cusr)
        status = g.status
        print(status)
    def stop(self):
        self.client.stop()
class App:
    def __init__(self):
        self.client = ClientTG(self)
        self.render = Render(self)

    def run(self):
        self.render.chat()
        self.render.panel()
        print("chat rendering completed")
        self.render.save()
        self.client.stop()


if __name__=='__main__':
    app=App()
    app.run()