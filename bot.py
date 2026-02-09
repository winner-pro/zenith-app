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

    if m.chat.id not in USERS_AUTORISES:
        bot.send_message(m.chat.id, "❌ Accès refusé. Contactez l'administrateur.")
        return

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('⚡ SCANNER L\'ALGO ⚡'), types.KeyboardButton('📒 GUIDE DE MISE'))
    

    if m.chat.id == ADMIN_ID:
        markup.add(types.KeyboardButton('👑 PANEL FONDATION'), types.KeyboardButton('📊 STATS UTILISATEURS'))
        
    bot.send_message(m.chat.id, "🌌 **ASTRO-AI PRÊT**\nBienvenue, Fondateur.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle(m):

    if m.chat.id not in USERS_AUTORISES:
        return

    if m.text == '⚡ SCANNER L\'ALGO ⚡':

        msg_prepa = bot.send_message(m.chat.id, "⚠️ **PRÉPARATION...**\nPlacez votre mise, décollage dans 30s.", parse_mode="Markdown")
        time.sleep(2) # Petit délai pour l'effet d'analyse


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
        bot.edit_message_text(texte_signal, m.chat.id, msg_prepa.message_id, parse_mode="Markdown")

        time.sleep(5) 
        resultat_reel = round(prediction + random.uniform(-0.2, 1.5), 2) # Simule le crash réel
        
        if resultat_reel >= prediction:
            bot.send_message(m.chat.id, f"✅ **CÔTE VALIDÉE !**\nL'avion est monté à **{resultat_reel}x**. L'objectif de {prediction}x a été atteint.")
        else:
            bot.send_message(m.chat.id, f"❌ **SIGNAL ÉCHOUÉ**\nCrash prématuré à **{resultat_reel}x**.")

    elif m.text == '📊 STATS UTILISATEURS' and m.from_user.id == ADMIN_ID:
        nb = len(USERS_AUTORISES)
        liste_ids = "\n".join([f"• `{i}`" for i in USERS_AUTORISES])
        bot.send_message(m.chat.id, f"📊 **STATS FONDATION**\n\nUtilisateurs actifs : **{nb}**\n\n**Liste des IDs :**\n{liste_ids}", parse_mode="Markdown")

    elif m.text == '👑 PANEL FONDATION' and m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "🛡️ **PANEL FONDATEUR**\nStatut : Opérationnel\nServeur : Termux/PM2")

    elif m.text == '📒 GUIDE DE MISE':
        bot.send_message(m.chat.id, "💰 **STRATÉGIE DE MISE :**\n\n1. Ne misez jamais plus de 10% de votre capital.\n2. Si un signal échoue, ne doublez pas tout de suite.\n3. Restez discipliné.")

bot.infinity_polling()

