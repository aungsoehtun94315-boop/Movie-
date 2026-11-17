import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging သတ်မှတ်ချက်
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ပေးထားသော လင့်ခ်များနှင့် ဇာတ်ကားအမျိုးအစားများ 
MOVIE_DATABASE = {
    # အော်ကား လင့်ခ်
    "အော်ကား": "https://t.me/paradisechannel13[span_0](start_span)[span_0](end_span)",
    "paradise channel": "https://t.me/paradisechannel13[span_1](start_span)[span_1](end_span)",
    
    # စစ်ကား လင့်ခ်
    "စစ်ကား": "https://t.me/moz1092",
    "war movie": "https://t.me/moz1092",
    
    # Change your life / Anime လင့်ခ်
    "change your life": "https://t.me/animemmsubaynlunou",
    "anime": "https://t.me/animemmsubaynlunou"
}

# /start Command အတွက်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"မင်္ဂလာပါ {user_name} 🙏\n\n"
        "ဒီ Bot က ဇာတ်ကားရှာဖွေပေးတဲ့ Bot ဖြစ်ပါတယ်။\n"
        "ကြည့်ချင်တဲ့ ဇာတ်ကားအမျိုးအစားကို ရိုက်ထည့်ပြီး ရှာနိုင်ပါတယ်[span_2](start_span)[span_2](end_span)။\n\n"
        "ရရှိနိုင်သော အမျိုးအစားများ:\n"
        "👉 *စစ်ကား*\n"
        "👉 *အော်ကား*\n"
        "👉 *Change your life / Anime*\n\n"
        "ဥပမာ - `စစ်ကား` လို့ ရိုက်ရှာပါ။"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# ဇာတ်ကားအသစ် ထည့်သွင်းရန် Command (Admin သုံးရန် - /add ဇာတ်ကားနာမည် - လင့်ခ်)
async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/add", "").strip()
        if "-" not in text:
            await update.message.reply_text("❌ ပုံစံမှားနေပါတယ်။ ဤသို့ထည့်ပါ:\n`/add ဇာတ်ကားနာမည် - လင့်ခ်`", parse_mode="Markdown")
            return
        
        movie_name, movie_link = text.split("-", 1)
        movie_name = movie_name.strip().lower()
        movie_link = movie_link.strip()
        
        MOVIE_DATABASE[movie_name] = movie_link
        await update.message.reply_text(f"✅ အောင်မြင်ပါသည်! '{movie_name}' ကို Database ထဲသို့ ထည့်သွင်းပြီးပါပြီ။")
    except Exception as e:
        await update.message.reply_text("❌ မှားယွင်းမှု ရှိနေပါသည်။ ကျေးဇူးပြု၍ ပုံစံမှန်ကန်စွာ ရိုက်ထည့်ပါ။")

# စာသား (Message) ပို့လာပါက ဇာတ်ကားရှာပေးမည့် Function
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    
    found_links = []
    for title, link in MOVIE_DATABASE.items():
        if query in title:
            found_links.append(f"🎬 *{title.title()}*\n🔗 Link: {link}")
    
    if found_links:
        response_text = "ရှာတွေ့ရှိသော ဇာတ်ကားများ:\n\n" + "\n\n".join(found_links)
        await update.message.reply_text(response_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ တောင်းပန်ပါတယ်။ ဒီအမျိုးအစားကို ရှာမတွေ့ပါ။ 'စစ်ကား' သို့မဟုတ် 'အော်ကား' ဟု တိကျစွာ ရိုက်ရှာကြည့်ပါ။")

def main():
    # သင့်ရဲ့ Bot Token
    TOKEN = "8371132363:AAHrSUhQJUsy5UUOSPFNLx-SyqqBtk5LDd4"
    
    # Application တည်ဆောက်ခြင်း
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers များ ချိတ်ဆက်ခြင်း
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_movie))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_movie))
    
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
    