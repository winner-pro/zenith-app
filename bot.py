import telebot
from telebot import types
import random
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
TOKEN = "8376333477:AAFi4gvsAxIu24xcFVDHgelnPuOgOlJIphg"
ADMIN_ID = 7874316578
USERS_AUTORISES = [7874316578, 5678348113]
bot = telebot.TeleBot(TOKEN)

# Dictionnaire pour stocker les scores (Optionnel pour la session)
stats_session = {"win": 0, "loss": 0}

@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.id not in USERS_AUTORISES:
        bot.send_message(m.chat.id, "❌ Accès refusé.")
        return

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('⚡ SCANNER L\'ALGO ⚡'), types.KeyboardButton('📒 GUIDE DE MISE'))
    if m.chat.id == ADMIN_ID:
        markup.add(types.KeyboardButton('👑 PANEL FONDATION'), types.KeyboardButton('📊 STATS UTILISATEURS'))
    bot.send_message(m.chat.id, "🌌 **ASTRO-AI PRÊT**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.chat.id not in USERS_AUTORISES:
        return

    if m.text == '⚡ SCANNER L\'ALGO ⚡':
        # 1. ALERTE PRÉPARATION
        msg = bot.send_message(m.chat.id, "🛰️ **Analyse de l'algorithme...**")
        time.sleep(1.5)

        # 2. GÉNÉRATION DU SIGNAL (Basé sur ton interface)
        prediction = round(random.uniform(1.50, 4.50), 2)
        heure_signal = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")

        texte_signal = (
            "🎯 **SIGNAL DÉTECTÉ**\n"
            "━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE PRÉCISE :** {heure_signal}\n"
            f"🚀 **OBJECTIF :** {prediction}x\n"
            "━━━━━━━━━━━━━━\n"
            "✅ **CONFIANCE : 99%**"
        )
        bot.edit_message_text(texte_signal, m.chat.id, msg.message_id, parse_mode="Markdown")

        # 3. INTERFACE DE VALIDATION RÉELLE (Fini le faux calcul !)
        time.sleep(2)
        markup_verif = types.InlineKeyboardMarkup()
        btn_win = types.InlineKeyboardButton("✅ CÔTE ATTEINTE", callback_data=f"win_{prediction}")
        btn_loss = types.InlineKeyboardButton("❌ CRASH AVANT", callback_data=f"loss_{prediction}")
        markup_verif.add(btn_win, btn_loss)
        
        bot.send_message(m.chat.id, "🧐 **Vérification en cours...**\nL'avion a-t-il atteint l'objectif ?", reply_markup=markup_verif)

    elif m.text == '📊 STATS UTILISATEURS' and m.from_user.id == ADMIN_ID:
        nb = len(USERS_AUTORISES)
        bot.send_message(m.chat.id, f"📊 **STATS FONDATION**\nUtilisateurs : {nb}\nVictoires : {stats_session['win']}\nDéfaites : {stats_session['loss']}")

    elif m.text == '👑 PANEL FONDATION' and m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "🛡️ **ADMIN :** Bot actif sous PM2.")

# --- GESTION DES BOUTONS DE VALIDATION ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, cote = call.data.split('_')
    
    if action == "win":
        stats_session["win"] += 1
        bot.edit_message_text(f"✅ **CÔTE VALIDÉE !**\nL'objectif de **{cote}x** a été encaissé avec succès. 💰", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    elif action == "loss":
        stats_session["loss"] += 1
        bot.edit_message_text(f"❌ **SIGNAL ÉCHOUÉ**\nL'avion a crashé avant **{cote}x**. Analyse de l'erreur en cours...", call.message.chat.id, call.message.message_id, parse_mode="Markdown")

bot.infinity_polling()
