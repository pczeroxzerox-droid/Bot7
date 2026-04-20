import telebot
import yt_dlp

API_TOKEN = 'YOUR_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Welcome to the YouTube Video Downloader Bot!")

@bot.message_handler(commands=['download'])
def download_video(message):
    url = message.text.split(' ')[1]
    options = {
        'format': 'best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    bot.send_message(message.chat.id, "Download completed!")

bot.polling()