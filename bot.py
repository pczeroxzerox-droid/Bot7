import os
import json
import datetime
import secrets
import telebot
from telebot import types
import yt_dlp

# ================= CONFIG =================
API_TOKEN = os.getenv("BOT_API_TOKEN", "8311544685:AAHyxtexwj_bPCutRhM1mfvWjLNMhfomn9M")
ADMIN_ID = int(os.getenv("ADMIN_ID", 8210146346))

CHANNEL_1 = "@samiedit9"
CHANNEL_2 = "@primiumboss29"

DB_FILE = "bot_data.json"

VIDEO_LIMIT = 3

bot = telebot.TeleBot(API_TOKEN)

# ================= DATABASE =================
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(user_data, f, indent=2)

user_data = load_db()

# ================= USER =================
def get_user(uid):
    uid = str(uid)

    if uid not in user_data:
        user_data[uid] = {
            "video": 0,
            "date": str(datetime.date.today()),
            "premium": False,
            "ref": f"REF{secrets.token_hex(3)}",
            "referred_by": None,
            "ref_count": 0
        }
        save_db()

    return user_data[uid]

# ================= RESET =================
def reset(uid):
    u = get_user(uid)
    today = str(datetime.date.today())

    if u["date"] != today:
        u["video"] = 0
        u["date"] = today
        save_db()

# ================= CHANNEL CHECK =================
def check_join(uid):
    try:
        m1 = bot.get_chat_member(CHANNEL_1, uid)
        m2 = bot.get_chat_member(CHANNEL_2, uid)

        if m1.status in ["left", "kicked"] or m2.status in ["left", "kicked"]:
            bot.send_message(uid, f"⚠️ আগে দুইটা চ্যানেল join করুন:\n{CHANNEL_1}\n{CHANNEL_2}")
            return False
        return True
    except:
        return True

# ================= MENU =================
def menu(uid):
    m = types.InlineKeyboardMarkup(row_width=2)

    m.add(types.InlineKeyboardButton("🎵 TikTok ভিডিও", callback_data="video"))

    if int(uid) == ADMIN_ID:
        m.add(types.InlineKeyboardButton("👑 Admin Panel", callback_data="admin"))

    return m

# ================= START =================
@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.chat.id
    reset(uid)

    u = get_user(uid)

    bot.send_message(
        uid,
        f"👋 স্বাগতম\n\n🎵 TikTok ভিডিও বাকি: {VIDEO_LIMIT - u['video']}\n💎 প্রিমিয়াম: {'হ্যাঁ ✅' if u['premium'] else 'না ❌'}"
        ,
        reply_markup=menu(uid)
    )

# ================= CALLBACK =================
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid = c.message.chat.id
    u = get_user(uid)

    bot.answer_callback_query(c.id)

    # -------- TIKTOK VIDEO --------
    if c.data == "video":

        if not check_join(uid):
            return

        if u["video"] >= VIDEO_LIMIT and not u["premium"]:
            bot.send_message(uid, "❌ আজকের লিমিট শেষ! 💎 প্রিমিয়াম নিন আনলিমিটেড ভিডিওর জন্য")
            return

        bot.send_message(uid, "🎵 TikTok লিংক পাঠাও (URL):")
        bot.register_next_step_handler(c.message, download_tiktok)

    # -------- ADMIN PANEL --------
    elif c.data == "admin":
        if uid != ADMIN_ID:
            return

        total = len(user_data)
        premium = sum(1 for x in user_data.values() if x["premium"])

        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(types.InlineKeyboardButton("🔍 ইউজার খুঁজুন", callback_data="find_user"))
        m.add(types.InlineKeyboardButton("💎 প্রিমিয়াম দিন", callback_data="give_premium"))
        m.add(types.InlineKeyboardButton("❌ প্রিমিয়াম সরান", callback_data="remove_premium"))

        bot.send_message(uid, f"👑 ADMIN PANEL\n\n👥 মোট ইউজার: {total}\n💎 প্রিমিয়াম ইউজার: {premium}", reply_markup=m)

    # -------- FIND USER --------
    elif c.data == "find_user":
        if uid != ADMIN_ID:
            return
        bot.send_message(uid, "🔍 ইউজার ID পাঠাও:")
        bot.register_next_step_handler(c.message, find_user_handler)

    # -------- GIVE PREMIUM --------
    elif c.data == "give_premium":
        if uid != ADMIN_ID:
            return
        bot.send_message(uid, "💎 যাকে প্রিমিয়াম দিতে চান তার ID পাঠাও:")
        bot.register_next_step_handler(c.message, give_premium_handler)

    # -------- REMOVE PREMIUM --------
    elif c.data == "remove_premium":
        if uid != ADMIN_ID:
            return
        bot.send_message(uid, "❌ যাকে প্রিমিয়াম সরাতে চান তার ID পাঠাও:")
        bot.register_next_step_handler(c.message, remove_premium_handler)

# ================= TIKTOK DOWNLOAD =================
def download_tiktok(msg):
    uid = msg.chat.id
    u = get_user(uid)
    link = msg.text.strip()

    if "tiktok.com" not in link:
        bot.send_message(uid, "❌ এটা TikTok লিংক নয়! সঠিক TikTok URL পাঠাও")
        return

    bot.send_message(uid, "⏳ ডাউনলোড হচ্ছে... অপেক্ষা করুন 🎵")

    try:
        file = f"tiktok_{uid}.mp4"

        ydl_opts = {
            "format": "best",
            "outtmpl": file,
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        with open(file, "rb") as f:
            bot.send_video(uid, f)

        os.remove(file)

        if not u["premium"]:
            u["video"] += 1
            save_db()

        bot.send_message(uid, "✅ ভিডিও পাঠানো হয়েছে! 🎉")

    except Exception as e:
        bot.send_message(uid, f"❌ ত্রুটি: {str(e)}")

# ================= ADMIN HANDLERS =================
def find_user_handler(msg):
    if msg.chat.id != ADMIN_ID:
        return
    
    try:
        uid = msg.text.strip()
        if uid in user_data:
            u = user_data[uid]
            info = f"""👤 ইউজার তথ্য:\n\nID: {uid}\n🎬 ভিডিও ডাউনলোড: {u['video']}\n💎 প্রিমিয়াম: {'হ্যাঁ ✅' if u['premium'] else 'না ❌'}\n📅 তারিখ: {u['date']}\n🔗 রেফারেল: {u['ref']}"""
            bot.send_message(msg.chat.id, info)
        else:
            bot.send_message(msg.chat.id, "❌ এই ইউজার পাওয়া যায়নি")
    except:
        bot.send_message(msg.chat.id, "❌ ত্রুটি! সঠিক ইউজার ID পাঠান")


def give_premium_handler(msg):
    if msg.chat.id != ADMIN_ID:
        return
    
    try:
        uid = msg.text.strip()
        if uid in user_data:
            user_data[uid]["premium"] = True
            save_db()
            bot.send_message(msg.chat.id, f"✅ {uid} কে প্রিমিয়াম দেওয়া হয়েছে")
        else:
            bot.send_message(msg.chat.id, "❌ ইউজার পাওয়া যায়নি")
    except:
        bot.send_message(msg.chat.id, "❌ ত্রুটি!")

def remove_premium_handler(msg):
    if msg.chat.id != ADMIN_ID:
        return
    
    try:
        uid = msg.text.strip()
        if uid in user_data:
            user_data[uid]["premium"] = False
            save_db()
            bot.send_message(msg.chat.id, f"✅ {uid} এর প্রিমিয়াম সরানো হয়েছে")
        else:
            bot.send_message(msg.chat.id, "❌ ইউজার পাওয়া যায়নি")
    except:
        bot.send_message(msg.chat.id, "❌ ত্রুটি!")

# ================= RUN =================
print("🚀 TIKTOK BOT চালু হয়েছে...")
bot.infinity_polling()
