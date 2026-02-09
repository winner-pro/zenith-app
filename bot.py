import telebot
from telebot import types
import random
import time
from datetime import datetime, timedelta

TOKEN = "8376333477:AAFi4gvsAxIu24xcFVDHgelnPuOgOlJIphg"
ADMIN_ID = 7874316578
USERS_AUTORISES = [7874316578, 5678348113]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('⚡ SCANNER L\'ALGO ⚡'), types.KeyboardButton('📒 GUIDE DE MISE'))
    if m.chat.id == ADMIN_ID:
        markup.add(types.KeyboardButton('👑 PANEL FONDATION'))
    bot.send_message(m.chat.id, "🌌 **ASTRO-AI PRÊT**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.text == '⚡ SCANNER L\'ALGO ⚡':
        msg = bot.send_message(m.chat.id, "🛰️ **Analyse en cours...**")
        time.sleep(1)
        
        prediction = round(random.uniform(1.50, 4.50), 2)
        heure = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")

        texte_final = (
            "🎯 **SIGNAL DÉTECTÉ**\n"
            "━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE :** {heure}\n"
            f"🚀 **OBJECTIF :** {prediction}x\n"
            "━━━━━━━━━━━━━━\n"
            "✅ **CONFIANCE : 99%**"
        )
        bot.edit_message_text(texte_final, m.chat.id, msg.message_id, parse_mode="Markdown")

    elif m.text == '👑 PANEL FONDATION' and m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "📊 **ADMIN :** Bot en ligne sous PM2.")

    elif m.text == '📒 GUIDE DE MISE':
        bot.send_message(m.chat.id, "💰 **MISE :** 10% max.")

bot.infinity_polling()
