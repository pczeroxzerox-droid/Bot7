# 🎬 YouTube Video Downloader Bot

একটি শক্তিশালী টেলিগ্রাম বট যা YouTube থেকে ভিডিও ডাউনলোড করে।

## ✨ ফিচার

- 🎬 YouTube ভিডিও ডাউনলোড (MP4)
- 💎 প্রিমিয়াম সিস্টেম (আনলিমিটেড ডাউনলোড)
- 📊 দৈনিক লিমিট (৩টি ভিডিও/দিন ফ্রি)
- 👑 অ্যাডমিন প্যানেল
- 🔐 চ্যানেল ভেরিফিকেশন
- 🔗 রেফারেল সিস্টেম
- 💾 ডাটা পার্সিসটেন্স

## 🚀 Railway এ ডিপ্লয় করুন

### ধাপ ১: Railway.app এ যান
👉 https://railway.app

### ধাপ ২: নতুন প্রজেক্ট তৈরি করুন
1. **New Project** ক্লিক করুন
2. **Deploy from GitHub repo** নির্বাচন করুন
3. **Bot7** রেপো সিলেক্ট করুন
4. **Deploy** ক্লিক করুন

### ধাপ ৩: Environment Variables সেট করুন
Railway Dashboard এ **Variables** ট্যাবে:

```env
BOT_API_TOKEN=8615288381:AAGwDHusKLlS4zTrf6IOiFuLLf9DICYcOCM
ADMIN_ID=8210146346
```

### ধাপ ৪: ডিপ্লয় সম্পন্ন!
✅ বট স্বয়ংক্রিয়ভাবে চালু হবে এবং ২৪/৭ চলবে

## 🎯 বটের মেনু

```
🎬 Video     - YouTube ভিডিও ডাউনলোড
👑 Admin     - অ্যাডমিন প্যানেল (শুধু ADMIN_ID)
```

## 📋 বাটন এবং ফিচার

| বাটন | কাজ | লিমিট |
|------|------|--------|
| 🎬 Video | YouTube থেকে MP4 ডাউনলোড | ৩টি/দিন (ফ্রি) |
| 👑 Admin | মোট ইউজার এবং প্রিমিয়াম দেখুন | শুধু ADMIN_ID |

## 💾 ডাটা স্ট্রাকচার

```json
{
  "ব্যবহারকারী_আইডি": {
    "video": 1,
    "date": "2026-04-22",
    "premium": false,
    "ref": "REFxxxxxx",
    "referred_by": null,
    "ref_count": 0
  }
}
```

## 🔧 লোকালি চালাতে

```bash
# ডিপেন্ডেন্সি ইন্সটল করুন
pip install -r requirements.txt

# পরিবেশ ভেরিয়েবল সেট করুন
export BOT_API_TOKEN="আপনার_টোকেন"
export ADMIN_ID="আপনার_আইডি"

# বট চালান
python bot.py
```

## 📄 লাইসেন্স
MIT License

## 👤 ডেভেলপার
[@pczeroxzerox-droid](https://github.com/pczeroxzerox-droid)

---

**🌟 স্টার দিতে ভুলবেন না!**
