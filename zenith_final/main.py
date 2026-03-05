#!/usr/bin/env python3
import telebot, sqlite3, random, time, string
from telebot import types
from datetime import datetime, timedelta
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# ==========================================
# ⚙️ CONFIGURATION DE L'EMPEREUR
# ==========================================
BOT_TOKEN = "8376333477:AAH4RiUUpdq6hNizQ-SjqE7WP5F-vMatlyU" 
ADMIN_ID = 7874316578
DB = "zenith_empire_v9.db"
URL_SATELLITE = "https://verdant-praline-69fb6e.netlify.app"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# --- État Global du Marché (Persistance RAM) ---
MARKET_STATUS = "STABLE" # DANGER, STABLE, ELITE

# ==========================================
# 🗄️ BASE DE DONNÉES & RANGS
# ==========================================
LIMITS = {"tester": 5, "VIP": 50, "👑 FONDATEUR": 999}

def db_q(query, params=(), fetchone=False):
    with sqlite3.connect(DB, check_same_thread=False) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.fetchone() if fetchone else None

def init_db():
    db_q("""CREATE TABLE IF NOT EXISTS users (
        tid TEXT PRIMARY KEY, uname TEXT, tier TEXT DEFAULT 'tester', 
        wallet REAL DEFAULT 0.0, current_bet REAL DEFAULT 0.0, 
        daily_scans INTEGER DEFAULT 0, last_scan_date TEXT, banned INTEGER DEFAULT 0)""")
    db_q("CREATE TABLE IF NOT EXISTS codes (code TEXT PRIMARY KEY, type TEXT, used INTEGER DEFAULT 0)")
init_db()

# ==========================================
# 🧠 MOTEUR DE PRÉDICTION AVANCÉ (SHA-512 SIM)
# ==========================================
def calculate_probability():
    """Simule l'analyse de la courbe de perte : P(X > x) = 1/x * (1 - e)"""
    now = datetime.now()
    # Cycle Horaire : Boost entre 02:00 et 04:00 GMT
    hour_boost = 1.5 if 2 <= now.hour <= 4 else 1.0
    
    global MARKET_STATUS
    if MARKET_STATUS == "DANGER": return None, 0, "🔴 DANGER"
    if MARKET_STATUS == "ELITE": return round(random.uniform(5.0, 45.0), 2), 98, "💎 ÉLITE"
    
    # Logique Standard v5.8.2
    chance = random.randint(1, 100)
    if chance > 75:
        return round(random.uniform(2.5, 18.0) * hour_boost, 2), random.randint(94, 97), "🔥 V5-VIGUEUR"
    return round(random.uniform(1.4, 2.2), 2), random.randint(91, 95), "🛡️ V5-STABLE"

# ==========================================
# 🎬 INTERFACE & ANIMATION HUMANISÉE
# ==========================================
def run_hacking_animation(chat_id):
    steps = [
        ("📡 <b>SCANNING PORT 443...</b>\n<code>[▒▒▒▒▒▒▒▒▒▒] 12%</code>", 0.5),
        ("🕵️ <b>INJECTION HASH SHA-512...</b>\n<code>[███▒▒▒▒▒▒▒] 38%</code>", 0.8),
        ("🔓 <b>BYPASSING 1WIN WAF...</b>\n<code>[███████▒▒▒] 74%</code>", 0.6),
        ("🧠 <b>EXTRACTION DES GRAINES...</b>\n<code>[██████████] 100%</code>", 0.4)
    ]
    msg = bot.send_message(chat_id, steps[0][0])
    for text, delay in steps[1:]:
        time.sleep(delay)
        try: bot.edit_message_text(text, chat_id, msg.message_id)
        except: pass
    return msg.message_id

def main_menu(uid):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb.add("⚡ SCAN ÉLITE", "🛰️ SCAN SATELLITE")
    kb.add("💰 MISE", "📊 WALLET")
    kb.add("🔑 ACTIVER CODE", "📡 INTEL")
    if str(uid) == str(ADMIN_ID): kb.add("🛠 ADMIN", "🚨 SIGNALER ÉTAT")
    return kb

# ==========================================
# ⚡ GESTION DES COMMANDES
# ==========================================
@bot.message_handler(commands=["start"])
def start(m):
    tid = str(m.chat.id)
    db_q("INSERT OR IGNORE INTO users (tid, uname) VALUES (?, ?)", (tid, m.from_user.first_name))
    if tid == str(ADMIN_ID): db_q("UPDATE users SET tier = '👑 FONDATEUR' WHERE tid=?", (tid,))
    u = db_q("SELECT tier FROM users WHERE tid=?", (tid,), True)
    bot.send_message(tid, f"<b>── 〈 ZENITH EMPIRE v9 〉 ──</b>\n\nAgent: <b>{m.from_user.first_name}</b>\nStatut Marché: <code>{MARKET_STATUS}</code>", reply_markup=main_menu(tid))

@bot.message_handler(func=lambda m: m.text == "⚡ SCAN ÉLITE")
def scan(m):
    tid = str(m.chat.id)
    today = datetime.now().strftime("%Y-%m-%d")
    u = db_q("SELECT tier, current_bet, daily_scans, last_scan_date, banned, wallet FROM users WHERE tid=?", (tid,), True)

    if u[4] == 1: return bot.send_message(tid, "💀 Accès révoqué.")
    if u[1] <= 0: return bot.send_message(tid, "❌ Définissez une mise (💰 MISE).")

    # Vérification des limites
    scans_today = u[2] if u[3] == today else 0
    if scans_today >= LIMITS.get(u[0], 5): return bot.send_message(tid, "⚠️ Limite journalière atteinte.")

    mid = run_hacking_animation(tid)
    mult, conf, mode_name = calculate_probability()

    if mult is None:
        return bot.edit_message_text("🛑 <b>MARCHÉ VERROUILLÉ</b>\n\nLe Fondateur a détecté une série rouge. Scan impossible pour protéger votre capital.", tid, mid)

    db_q("UPDATE users SET daily_scans = ?, last_scan_date = ? WHERE tid = ?", (scans_today + 1, today, tid))
    t_crash = (datetime.now() + timedelta(seconds=random.randint(12, 38))).strftime("%H:%M:%S")
    
    res = (f"🎯 <b>EXTRACTION {mode_name}</b>\n"
           f"━━━━━━━━━━━━━━━\n"
           f"📈 COTE : <code>{mult}x</code>\n"
           f"🧠 FIABILITÉ : <code>{conf}%</code>\n"
           f"⏰ CRASH : <code>{t_crash}</code>\n"
           f"💰 GAIN : <code>{round(u[1]*mult, 2)} CFA</code>\n"
           f"━━━━━━━━━━━━━━━")
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("💎 ENCAISSÉ", callback_data=f"win_{round(u[1]*mult, 2)}"),
           types.InlineKeyboardButton("❌ PERDU", callback_data="loss"))
    bot.edit_message_text(res, tid, mid, reply_markup=mk)

# ==========================================
# 🚨 POSTE DE COMMANDEMENT (FONDATEUR)
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🚨 SIGNALER ÉTAT")
def report_status(m):
    if str(m.chat.id) != str(ADMIN_ID): return
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton("🔴 SÉRIE ROUGE (Bloquer)", callback_data="set_DANGER"),
        types.InlineKeyboardButton("🟢 SÉRIE STABLE (Normal)", callback_data="set_STABLE"),
        types.InlineKeyboardButton("🟣 SÉRIE ÉLITE (Cotes Hautes)", callback_data="set_ELITE")
    )
    bot.send_message(m.chat.id, "🛠 <b>COMMANDEMENT</b>\nQuelle est la tendance 1win actuelle ?", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_"))
def update_market(call):
    global MARKET_STATUS
    MARKET_STATUS = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"Mode {MARKET_STATUS} activé.")
    bot.edit_message_text(f"✅ <b>SYSTÈME AJUSTÉ</b>\nLe bot opère désormais en mode : <code>{MARKET_STATUS}</code>", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda m: m.text == "🛰️ SCAN SATELLITE")
def satellite_web(m):
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("👁️ TERMINAL CIA", web_app=types.WebAppInfo(url=URL_SATELLITE)))
    bot.send_message(m.chat.id, "🌐 <b>FLUX SATELLITE ACTIF</b>", reply_markup=mk)

# ==========================================
# 📋 GESTION PORTEFEUILLE & CODES
# ==========================================
@bot.callback_query_handler(func=lambda call: call.data.startswith("win_") or call.data == "loss")
def wallet_handle(call):
    tid = str(call.message.chat.id)
    if call.data.startswith("win_"):
        gain = float(call.data.split("_")[1])
        db_q("UPDATE users SET wallet = wallet + ? WHERE tid=?", (gain, tid))
        bot.answer_callback_query(call.id, "💰 Gain validé !")
    bot.edit_message_reply_markup(tid, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda m: m.text == "💰 MISE")
def set_bet(m):
    bot.register_next_step_handler(bot.send_message(m.chat.id, "💰 <b>Entrez la mise (CFA) :</b>"), save_bet)
def save_bet(m):
    try:
        db_q("UPDATE users SET current_bet=? WHERE tid=?", (float(m.text), str(m.chat.id)))
        bot.send_message(m.chat.id, f"✅ Mise : {m.text} CFA.")
    except: bot.send_message(m.chat.id, "❌ Chiffres requis.")

@bot.message_handler(func=lambda m: m.text == "📊 WALLET")
def wallet(m):
    u = db_q("SELECT tier, wallet, current_bet FROM users WHERE tid=?", (str(m.chat.id),), True)
    bot.send_message(m.chat.id, f"📊 <b>ETAT DES LIEUX</b>\n\nRang : <code>{u[0]}</code>\nPortefeuille : <code>{u[1]} CFA</code>\nMise active : <code>{u[2]} CFA</code>")

@bot.message_handler(func=lambda m: m.text == "🔑 ACTIVER CODE")
def ask_code(m):
    bot.register_next_step_handler(bot.send_message(m.chat.id, "🔑 <b>Code d'accès :</b>"), activate_code)
def activate_code(m):
    c = m.text.strip(); check = db_q("SELECT type FROM codes WHERE code = ? AND used = 0", (c,), True)
    if check:
        db_q("UPDATE codes SET used = 1 WHERE code = ?", (c,))
        db_q("UPDATE users SET tier = ? WHERE tid = ?", (check[0], str(m.chat.id)))
        bot.send_message(m.chat.id, f"🎉 Rang <b>{check[0]}</b> débloqué !")
    else: bot.send_message(m.chat.id, "❌ Code invalide.")

# --- Admin ---
@bot.message_handler(func=lambda m: m.text == "🛠 ADMIN")
def admin_panel(m):
    if str(m.chat.id) == str(ADMIN_ID):
        mk = types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("🎁 GÉNÉRER VIP", callback_data="gen_VIP"))
        bot.send_message(m.chat.id, "🛠 <b>CONSOLE</b>", reply_markup=mk)

@bot.callback_query_handler(func=lambda call: call.data == "gen_VIP")
def gen_vip(call):
    c = f"VIP-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    db_q("INSERT INTO codes (code, type) VALUES (?, 'VIP')", (c,))
    bot.send_message(call.message.chat.id, f"✅ Code : <code>{c}</code>")

# ==========================================
# 🚀 DÉMARRAGE
# ==========================================
if __name__ == "__main__":
    print(f"⛩️ ZENITH EMPIRE v9.2 ACTIF. MODE: {MARKET_STATUS}")
    bot.infinity_polling()

