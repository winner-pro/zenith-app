from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

def get_data():
    try:
        conn = sqlite3.connect('zenith_empire_v9.db')
        cursor = conn.cursor()
        # On récupère les 10 derniers signaux
        cursor.execute("SELECT timing, prediction, confiance, resultat FROM lucky_jet_signals ORDER BY id DESC LIMIT 10")
        signals = cursor.fetchall()
        # Calcul du Winrate
        cursor.execute("SELECT COUNT(*) FROM lucky_jet_signals WHERE resultat='GAGNÉ'")
        wins = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM lucky_jet_signals")
        total = cursor.fetchone()[0]
        wr = round((wins/total*100),1) if total > 0 else 0
        conn.close()
        return signals, wr, total
    except: return [], 0, 0

@app.route('/')
def index():
    signals, wr, total = get_data()
    rows = "".join([f"<tr><td>{s[0]}</td><td style='color:#fbbf24;font-weight:bold'>{s[1]}x</td><td>{s[2]}%</td><td style='color:{'#22c55e' if s[3]=='GAGNÉ' else '#ef4444'}'>{s[3]}</td></tr>" for s in signals])
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ZENITH RADAR V11</title>
        <style>
            body {{ background: #050505; color: #e5e7eb; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; display: flex; justify-content: center; }}
            .app-card {{ width: 100%; max-width: 450px; background: #0f1012; border: 1px solid #fbbf24; border-radius: 20px; padding: 15px; box-shadow: 0 0 30px rgba(251, 191, 36, 0.1); }}
            .header {{ text-align: center; border-bottom: 1px solid #1f2937; padding-bottom: 15px; margin-bottom: 15px; }}
            .title {{ color: #fbbf24; font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; }}
            .stats-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }}
            .stat-box {{ background: #16181d; padding: 12px; border-radius: 12px; text-align: center; border: 1px solid #2d2f36; }}
            .stat-val {{ font-size: 1.5rem; font-weight: bold; display: block; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
            th {{ color: #9ca3af; text-align: left; padding: 8px; border-bottom: 1px solid #1f2937; }}
            td {{ padding: 12px 8px; border-bottom: 1px solid #16181d; }}
            .badge {{ background: rgba(251, 191, 36, 0.1); color: #fbbf24; padding: 2px 8px; border-radius: 5px; font-size: 10px; }}
        </style>
    </head>
    <body>
        <div class="app-card">
            <div class="header">
                <div class="title">🛰️ ZENITH RADAR V11</div>
                <span class="badge">SYSTÈME IA ALPHA CONNECTÉ</span>
            </div>
            <div class="stats-row">
                <div class="stat-box"><small style="color:#9ca3af">PRÉCISION</small><span class="stat-val" style="color:#22c55e">{wr}%</span></div>
                <div class="stat-box"><small style="color:#9ca3af">SCANS</small><span class="stat-val">{total}</span></div>
            </div>
            <table>
                <thead><tr><th>HEURE</th><th>CIBLE</th><th>IA</th><th>RÉSULTAT</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        <script>setTimeout(() => location.reload(), 5000);</script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

