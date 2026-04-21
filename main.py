import os
import telebot
from yt_dlp import YoutubeDL
from flask import Flask
from threading import Thread

# لێرە توکنێ خۆ یێ دروست دانێ
API_TOKEN = 8465727601:AAHDsLKvbwwyXYtC7YG49HGstSAqiGD5A4s
bot = telebot.TeleBot(API_TOKEN)

# ئەڤ بەشە بۆ هندێیە کو بۆت نەکەڤیتە خەوێ (Keep Alive)
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلاڤ! لینکا ڤیدیۆیێ فرێکە دا بۆتە دابەزینم.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        bot.reply_to(message, "کێمەک چاڤەڕێ بە... ⏳")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove('video.mp4')
        except Exception as e:
            bot.reply_to(message, "ببورە، کێشەیەک هەبوو.")

if __name__ == "__main__":
    keep_alive()
    print("بۆت کار دەکات...")
    bot.polling()
