import telebot
from telebot import types
import sqlite3
import datetime
import random
import time
import string

# --- CONFIGURATION ---
TOKEN = "8376333477:AAEAyJT-b1yuKAa5W3FSyEJ3WLAIdjdD3lk"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = "7874316578"  # Ton ID, Gnohou

# --- FONCTION BASE DE DONNÉES ---
def query_db(query, args=(), one=False):
    try:
        conn = sqlite3.connect('zenith_empire_v9.db')
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        conn.commit()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        print(f"Erreur DB : {e}")
        return None

# --- VÉRIFICATION ACCÈS ---
def has_access(user_id):
    if str(user_id) == ADMIN_ID: return True
    user = query_db("SELECT expiration FROM users WHERE user_id=?", (str(user_id),), one=True)
    if user:
        try:
            exp_date = datetime.datetime.strptime(user[0], "%Y-%m-%d %H:%M")
            return datetime.datetime.now() < exp_date
        except: return False
    return False

# --- COMMANDE START & MENU BOUTONS ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    
    # Enregistrement auto du Fondateur (Toi)
    if user_id == ADMIN_ID:
        query_db("INSERT OR IGNORE INTO users (user_id, nom, niveau, expiration) VALUES (?, ?, ?, ?)", 
                 (user_id, user_name, "FONDATEUR", "2099-01-01 00:00"))

    # Création du Menu Principal (Clavier fixe)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🚀 SCAN ÉLITE"), 
        types.KeyboardButton("👤 MON PROFIL"),
        types.KeyboardButton("💎 DEVENIR VIP"),
        types.KeyboardButton("📢 CANAL OFFICIEL")
    )
    
    welcome = (
        f"🛰️ **SYSTÈME ZENITH V11 CONNECTÉ**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Bienvenue, {user_name}.\n"
        f"Statut : `OPÉRATIONNEL` ✅\n"
        f"Intelligence : `ACTIVE` 🧠\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

# --- FONCTION SCAN ÉLITE ---
@bot.message_handler(func=lambda m: m.text == "🚀 SCAN ÉLITE")
def scan_elite(message):
    user_id = str(message.from_user.id)
    if not has_access(user_id):
        bot.reply_to(message, "❌ **ACCÈS REFUSÉ**\nContactez @Gnohou pour une licence.")
        return

    user_data = query_db("SELECT niveau FROM users WHERE user_id=?", (user_id,), one=True)
    niveau = user_data[0] if user_data else "BRONZE"

    sent_msg = bot.send_message(message.chat.id, "🛰️ `RECHERCHE DE SIGNAL...`", parse_mode='Markdown')
    time.sleep(1.5)

    # Intelligence de calcul
    if niveau in ["VIP", "FONDATEUR"]:
        pred = round(random.uniform(2.25, 6.50), 2)
        conf = random.randint(95, 99)
        tag = "🌟 [MODE VIP]"
    else:
        pred = round(random.uniform(1.30, 2.15), 2)
        conf = random.randint(85, 92)
        tag = "🥉 [MODE BRONZE]"

    now = datetime.datetime.now().strftime("%H:%M:%S")
    query_db("INSERT INTO lucky_jet_signals (timing, prediction, confiance, resultat) VALUES (?, ?, ?, ?)", 
             (now, pred, conf, "EN_ATTENTE"))

    res = (
        f"🎯 **SIGNAL DÉTECTÉ**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **STATUS :** `{tag}`\n"
        f"🕒 **HEURE :** `{now}`\n"
        f"📈 **CIBLE :** `{pred}x`\n"
        f"🔥 **FIABILITÉ :** `{conf}%`\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ GAGNÉ", callback_data="win"), 
               types.InlineKeyboardButton("❌ PERDU", callback_data="loss"))
    
    bot.edit_message_text(res, message.chat.id, sent_msg.message_id, reply_markup=markup, parse_mode='Markdown')

# --- FONCTION PROFIL ---
@bot.message_handler(func=lambda m: m.text == "👤 MON PROFIL")
def profile(message):
    user_id = str(message.from_user.id)
    u = query_db("SELECT niveau, expiration FROM users WHERE user_id=?", (user_id,), one=True)
    if u:
        text = f"👤 **PROFIL UTILISATEUR**\n\n🆔 ID : `{user_id}`\n🏆 Niveau : `{u[0]}`\n⏳ Expire : `{u[1]}`"
    else:
        text = "❌ Profil non trouvé. Tapez /start."
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- FONCTION VIP ---
@bot.message_handler(func=lambda m: m.text == "💎 DEVENIR VIP")
def vip_info(message):
    text = (
        "💎 **AVANTAGES ZENITH VIP**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "• Cotes élevées (> 2.50x)\n"
        "• Précision de 98%\n"
        "• Support 24h/7\n\n"
        "💰 *7 Jours : 5.000 FCFA*\n"
        "💰 *30 Jours : 15.000 FCFA*\n\n"
        "📩 Contact : @Gnohou"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- FONCTION CANAL ---
@bot.message_handler(func=lambda m: m.text == "📢 CANAL OFFICIEL")
def channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 REJOINDRE", url="https://t.me/ton_canal"))
    bot.send_message(message.chat.id, "📢 Suivez nos preuves ici :", reply_markup=markup)

# --- GÉNÉRATEUR DE CLÉS (ADMIN UNIQUEMENT) ---
@bot.message_handler(commands=['gen'])
def generate_key(message):
    if str(message.from_user.id) != ADMIN_ID: return
    try:
        parts = message.text.split()
        days, lvl = int(parts[1]), parts[2].upper()
        key = "ZNT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Ici on peut stocker la clé en DB si tu veux un système d'activation automatique
        bot.reply_to(message, f"🔑 **CLÉ GÉNÉRÉE**\n\n`{key}`\nDurée : {days}j\nNiveau : {lvl}")
    except:
        bot.reply_to(message, "Format: `/gen [jours] [niveau]`")

# --- BOUTONS RÉSULTATS ---
@bot.callback_query_handler(func=lambda call: call.data in ["win", "loss"])
def callback_res(call):
    res = "GAGNÉ" if call.data == "win" else "PERDU"
    query_db("UPDATE lucky_jet_signals SET resultat = ? WHERE id = (SELECT MAX(id) FROM lucky_jet_signals)", (res,))
    bot.answer_callback_query(call.id, f"Signal marqué comme {res}")
    bot.edit_message_text(call.message.text + f"\n\n🏁 **RÉSULTAT : {res}**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')

# --- DÉMARRAGE ---
print("🚀 Zenith V11 est en ligne !")
bot.polling(none_stop=True)

