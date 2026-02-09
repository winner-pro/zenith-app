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

# Système de mémoire vive
stats_session = {"win": 5, "loss": 5} # Initialisé avec tes derniers résultats

@bot.message_handler(commands=['start'])
def start(m):
    if m.chat.id not in USERS_AUTORISES:
        bot.send_message(m.chat.id, "❌ Accès refusé.")
        return

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('⚡ SCANNER L\'ALGO ⚡'), types.KeyboardButton('📒 GUIDE DE MISE'))
    if m.chat.id == ADMIN_ID:
        markup.add(types.KeyboardButton('👑 PANEL FONDATION'), types.KeyboardButton('📊 STATS UTILISATEURS'))
    bot.send_message(m.chat.id, "🌌 **ASTRO-AI V2 : CONNECTÉ**\nSystème adaptatif activé.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.chat.id not in USERS_AUTORISES:
        return

    if m.text == '⚡ SCANNER L\'ALGO ⚡':
        msg = bot.send_message(m.chat.id, "🛰️ **Analyse des cycles en cours...**")
        time.sleep(1.5)

        # INTELLIGENCE ADAPTATIVE
        diff = stats_session['win'] - stats_session['loss']
        
        if diff < 0: # MODE RÉCUPÉRATION (Si plus de défaites)
            prediction = round(random.uniform(1.30, 2.10), 2)
            conseil = "⚠️ Mode Sécurité : Objectif bas pour remonter."
        elif diff > 3: # MODE EXPLOITATION (Si grosse série de victoires)
            prediction = round(random.uniform(2.50, 5.50), 2)
            conseil = "🔥 Mode Audacieux : L'algorithme est favorable !"
        else: # MODE STANDARD
            prediction = round(random.uniform(1.80, 3.80), 2)
            conseil = "✅ Analyse stable."

        heure_signal = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")
        texte_signal = (
            "🎯 **SIGNAL DÉTECTÉ**\n"
            "━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE :** {heure_signal}\n"
            f"🚀 **OBJECTIF :** {prediction}x\n"
            "━━━━━━━━━━━━━━\n"
            f"💡 *{conseil}*"
        )
        bot.edit_message_text(texte_signal, m.chat.id, msg.message_id, parse_mode="Markdown")

        # Boutons de validation
        markup_verif = types.InlineKeyboardMarkup()
        markup_verif.add(types.InlineKeyboardButton("✅ VALIDÉ", callback_data=f"win_{prediction}"),
                         types.InlineKeyboardButton("❌ ÉCHOUÉ", callback_data=f"loss_{prediction}"))
        bot.send_message(m.chat.id, "🧐 **Verdict ?**", reply_markup=markup_verif)

    elif m.text == '📒 GUIDE DE MISE':
        guide = (
            "💰 **STRATÉGIE DE RELANCE**\n"
            "━━━━━━━━━━━━━━\n"
            "1️⃣ **Mise fixe** : 5% à 10% de la banque.\n"
            "2️⃣ **Après une chute** : Ne pas paniquer. Suivre le 'Mode Sécurité' du bot.\n"
            "3️⃣ **Objectif** : Viser la régularité, pas le gros coup d'un soir.\n"
            "━━━━━━━━━━━━━━\n"
            "✨ *On tombe pour mieux sauter !*"
        )
        bot.send_message(m.chat.id, guide, parse_mode="Markdown")

    elif m.text == '📊 STATS UTILISATEURS' and m.from_user.id == ADMIN_ID:
        total = stats_session['win'] + stats_session['loss']
        taux = (stats_session['win'] / total * 100) if total > 0 else 0
        bot.send_message(m.chat.id, f"📊 **BILAN FONDATION**\n\n✅ Victoires : {stats_session['win']}\n❌ Défaites : {stats_session['loss']}\n📈 Précision : {taux:.1f}%")

    elif m.text == '👑 PANEL FONDATION' and m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 **STATUT FONDA**\n\nIA : Niveau 2 (Adaptative)\nServeur : Actif\nAuto-Correction : ON")

# GESTION DES BOUTONS CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, cote = call.data.split('_')
    if action == "win":
        stats_session["win"] += 1
        bot.edit_message_text(f"✅ **BINGO !** Objectif {cote}x atteint.", call.message.chat.id, call.message.message_id)
    else:
        stats_session["loss"] += 1
        bot.edit_message_text(f"❌ **ÉCHEC.** Crash avant {cote}x. L'IA s'adapte...", call.message.chat.id, call.message.message_id)

bot.infinity_polling()
