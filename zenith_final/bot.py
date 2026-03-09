# --- AJOUT DES NOUVELLES FONCTIONNALITÉS ---

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    
    # Création du menu principal (Boutons en bas)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🚀 SCAN ÉLITE")
    btn2 = types.KeyboardButton("👤 MON PROFIL")
    btn3 = types.KeyboardButton("💎 DEVENIR VIP")
    btn4 = types.KeyboardButton("📢 CANAL OFFICIEL")
    markup.add(btn1, btn2, btn3, btn4)

    welcome_text = (
        f"🛰️ **BIENVENUE SUR ZENITH V11**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"L'IA la plus puissante pour vos analyses en temps réel.\n\n"
        f"Utilisez le menu ci-dessous pour commencer."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# --- FONCTIONNALITÉ : MON PROFIL ---
@bot.message_handler(func=lambda m: m.text == "👤 MON PROFIL")
def profile(message):
    user_id = str(message.from_user.id)
    user_data = query_db("SELECT niveau, expiration FROM users WHERE user_id=?", (user_id,), one=True)
    
    if user_data:
        niveau, exp = user_data
        msg = (
            f"👤 **VOTRE PROFIL**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 ID : `{user_id}`\n"
            f"🏆 NIVEAU : *{niveau}*\n"
            f"⏳ EXPIRE LE : `{exp}`\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
    else:
        msg = "❌ Aucun profil trouvé. Cliquez sur /start pour vous enregistrer."
    
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

# --- FONCTIONNALITÉ : DEVENIR VIP ---
@bot.message_handler(func=lambda m: m.text == "💎 DEVENIR VIP")
def buy_vip(message):
    markup = types.InlineKeyboardMarkup()
    # Remplace par ton propre lien Telegram ou ton contact
    markup.add(types.InlineKeyboardButton("💳 CONTACTER LE SUPPORT", url="https://t.me/Gnohou"))
    
    text = (
        f"💎 **OFFRES ZENITH VIP**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Signaux avec 98% de fiabilité\n"
        f"✅ Accès aux cotes > 2.00x\n"
        f"✅ Support Prioritaire 24/7\n\n"
        f"💰 **Tarifs :**\n"
        f"• 7 Jours : 5.000 FCFA\n"
        f"• 1 Mois : 15.000 FCFA\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

# --- FONCTIONNALITÉ : CANAL OFFICIEL ---
@bot.message_handler(func=lambda m: m.text == "📢 CANAL OFFICIEL")
def channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 REJOINDRE LE CANAL", url="https://t.me/ton_canal"))
    bot.send_message(message.chat.id, "Suivez nos résultats en direct ici :", reply_markup=markup)

