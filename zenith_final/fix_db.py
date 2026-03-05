import sqlite3

DB = "zenith_v6_final.db"

def patch():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try:
        # Ajout des colonnes manquantes dans la table users
        cursor.execute("ALTER TABLE users ADD COLUMN scans_today INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN last_scan_date TEXT")
        print("✅ Colonnes ajoutées à la table 'users'")
    except Exception as e:
        print(f"⚠️ Table users déjà à jour ou erreur : {e}")

    try:
        # Ajout de la colonne type dans la table codes
        cursor.execute("ALTER TABLE codes ADD COLUMN type TEXT DEFAULT 'tester'")
        print("✅ Colonne ajoutée à la table 'codes'")
    except Exception as e:
        print(f"⚠️ Table codes déjà à jour ou erreur : {e}")

    conn.commit()
    conn.close()
    print("🚀 Base de données prête pour Zenith v6.2.4 !")

if __name__ == "__main__":
    patch()

