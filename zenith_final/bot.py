import telebot
from telebot import types
import sqlite3
import datetime
import random
import time

# --- CONFIGURATION INITIALE ---
TOKEN = "8376333477:AAEAyJT-b1yuKAa5W3FSyEJ3WLAIdjdD3lk"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = "7874316578"  # Ton ID, Gnohou

# --- FONCTION DE GESTION BASE DE DONNÉES ---
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

# --- SYSTÈME DE VÉRIFICATION D'ACCÈS ---
def has_access(user_id):
    if str(user_id) == ADMIN_ID: return True
    user = query_db("SELECT expiration FROM users WHERE user_id=?", (str(user_id),), one=True)
    if user:
        try:
            exp_date = datetime.datetime.strptime(user[0], "%Y-%m-%d %H:%M")
            return datetime.datetime.now() < exp_date
        except:
            return False
    return False

# --- COMMANDE /START ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    
    # Enregistrement automatique du Fondateur
    if user_id == ADMIN_ID:
        query_db("INSERT OR IGNORE INTO users (user_id, nom, niveau, expiration) VALUES (?, ?, ?, ?)", 
                 (user_id, user_name, "FONDATEUR", "2099-01-01 00:00"))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🚀 SCAN ÉLITE"), types.KeyboardButton("📊 MES STATS"))
    markup.add(types.KeyboardButton("📡 ANALYSE LIVE"), types.KeyboardButton("⚙️ CONFIG"))
    
    welcome = (
        f"🛰️ **SYSTEME ZENITH V11 CONNECTÉ** 🛰️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Bienvenue, {user_name}.\n"
        f"Statut : `OPÉRATIONNEL` ✅\n"
        f"Base : `zenith_empire_v9.db` 🗄️\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

# --- LOGIQUE DE SCAN INTELLIGENT ---
@bot.message_handler(func=lambda m: m.text == "🚀 SCAN ÉLITE")
def scan_elite(message):
    user_id = str(message.from_user.id)
    
    if not has_access(user_id):
        bot.reply_to(message, "❌ **ACCÈS REFUSÉ**\nVotre licence est expirée.\nContactez @Gnohou pour activer.")
        return

    # Détection du niveau
    user_data = query_db("SELECT niveau FROM users WHERE user_id=?", (user_id,), one=True)
    niveau = user_data[0] if user_data else "BRONZE"

    sent_msg = bot.send_message(message.chat.id, "⚡ `INTERCEPTING DATA...`", parse_mode='Markdown')
    time.sleep(1)
    bot.edit_message_text("📡 `ANALYSE DES SEQUENCES IA...`", message.chat.id, sent_msg.message_id, parse_mode='Markdown')
    time.sleep(1)
    
    # Intelligence de prédiction selon le niveau
    if niveau in ["VIP", "FONDATEUR"]:
        pred = round(random.uniform(2.20, 5.50), 2)
        conf = random.randint(94, 99)
        tag = "🌟 [MODE VIP]"
    else:
        pred = round(random.uniform(1.35, 2.05), 2)
        conf = random.randint(84, 92)
        tag = "🥉 [MODE BRONZE]"

    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
    query_db("INSERT INTO lucky_jet_signals (timing, prediction, confiance, resultat) VALUES (?, ?, ?, ?)", 
             (timestamp, pred, conf, "EN_ATTENTE"))

    response = (
        f"🎯 **SIGNAL DÉTECTÉ - ZENITH V11**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **STATUS :** `{tag}`\n"
        f"🕒 **HEURE :** `{timestamp}`\n"
        f"📈 **CIBLE :** `{pred}x`\n"
        f"🔥 **FIABILITÉ :** `{conf}%`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Attendre la confirmation du radar.*"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ GAGNÉ", callback_data="win"), 
               types.InlineKeyboardButton("❌ PERDU", callback_data="loss"))
    
    bot.edit_message_text(response, message.chat.id, sent_msg.message_id, reply_markup=markup, parse_mode='Markdown')

# --- BOUTON CONFIG & ADMIN ---
@bot.message_handler(func=lambda m: m.text == "⚙️ CONFIG")
def config_handler(message):
    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ Ajouter Membre", callback_data="admin_add"))
        markup.add(types.InlineKeyboardButton("🧹 Vider Data", callback_data="clear_db"))
        bot.reply_to(message, "⚙️ **PANNEAU ADMIN**\nGérez les accès utilisateurs ici.", reply_markup=markup, parse_mode='Markdown')
    else:
        user = query_db("SELECT niveau, expiration FROM users WHERE user_id=?", (user_id,), one=True)
        status = f"📍 Niveau : `{user[0]}`\n⌛ Expire : `{user[1]}`" if user else "❌ Aucune licence."
        bot.reply_to(message, f"👤 **VOTRE PROFIL**\n\n{status}", parse_mode='Markdown')

# --- GESTION DES BOUTONS GAGNÉ/PERDU ---
@bot.callback_query_handler(func=lambda call: call.data in ["win", "loss"])
def callback_result(call):
    res_text = "GAGNÉ" if call.data == "win" else "PERDU"
    # Mise à jour du dernier signal
    query_db("UPDATE lucky_jet_signals SET resultat = ? WHERE id = (SELECT MAX(id) FROM lucky_jet_signals)", (res_text,))
    bot.answer_callback_query(call.id, f"Résultat enregistré : {res_text}")
    bot.edit_message_text(call.message.text + f"\n\n✅ **RÉSULTAT : {res_text}**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')

# --- COMMANDE ADMIN POUR AJOUTER (FORMAT: /add ID JOURS NIVEAU) ---
@bot.message_handler(commands=['add'])
def add_user_via_cmd(message):
    if str(message.from_user.id) != ADMIN_ID: return
    try:
        parts = message.text.split()
        uid, days, lvl = parts[1], int(parts[2]), parts[3].upper()
        exp = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
        query_db("INSERT OR REPLACE INTO users (user_id, expiration, niveau) VALUES (?, ?, ?)", (uid, exp, lvl))
        bot.reply_to(message, f"✅ Utilisateur `{uid}` ajouté !\nNiveau : `{lvl}`\nExpire : `{exp}`")
    except:
        bot.reply_to(message, "⚠️ Format : `/add ID JOURS NIVEAU` (ex: /add 12345 7 VIP)")

# --- DÉMARRAGE ---
print("🚀 Zenith V11 est en cours de lancement...")
bot.polling(none_stop=True)

