from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('zenith_empire_v9.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timing, prediction, confiance, resultat FROM lucky_jet_signals ORDER BY id DESC LIMIT 10")
    signals = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM lucky_jet_signals WHERE resultat='GAGNÉ'")
    wins = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lucky_jet_signals")
    total = cursor.fetchone()[0]
    wr = round((wins/total*100),1) if total > 0 else 0
    conn.close()
    return signals, wr, total

@app.route('/')
def index():
    signals, wr, total = get_data()
    rows = "".join([f"<tr><td>{s[0]}</td><td>{s[1]}x</td><td>{s[2]}%</td><td style='color:{'#22c55e' if s[3]=='GAGNÉ' else '#ef4444'}'>{s[3]}</td></tr>" for s in signals])
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ZENITH V11 - RADAR</title>
        <style>
            body {{ background: #020617; color: #38bdf8; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; border: 2px solid #38bdf8; border-radius: 20px; padding: 20px; box-shadow: 0 0 30px rgba(56, 189, 248, 0.3); }}
            h1 {{ text-shadow: 0 0 10px #38bdf8; font-size: 1.5rem; }}
            .stat-box {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat {{ background: #1e293b; padding: 10px; border-radius: 10px; min-width: 100px; }}
            .winrate {{ font-size: 1.8rem; color: #22c55e; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9rem; }}
            th {{ background: #38bdf8; color: #020617; padding: 10px; }}
            td {{ padding: 10px; border-bottom: 1px solid #1e293b; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛰️ ZENITH INTELLIGENCE V11</h1>
            <div class="stat-box">
                <div class="stat"><small>WINRATE</small><br><span class="winrate">{wr}%</span></div>
                <div class="stat"><small>SCANS</small><br><span>{total}</span></div>
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

