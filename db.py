import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("gastos.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTERGER,
            categoria TEXT,
            valor Real,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_gasto(user_id, categoria, valor):
    conn = sqlite3.connect("gastos.db")
    c = conn.cursor()
    c.execute('INSERT INTO gastos (user_id, categoria, valor, data) VALUES (?, ?, ?, ?)',
              (user_id, categoria, valor, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def obter_gastos_mes(user_id):
    conn = sqlite3.connect("gastos.db")
    c = conn.cursor()
    c.execute('''
        SELECT categoria, SUM(valor) FROM gastos
        WHERE user_id = ? AND strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY categoria
        ''', (user_id,))
    dados = c.fetchall()
    conn.close()
    return dados

def limpar_tudo(user_id):
    conn = sqlite3.connect("gastos.db")
    c = conn.cursor()
    c.execute("DELETE FROM gastos WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def limpar_categoria(user_id, categoria):
    conn = sqlite3.connect("gastos.db")
    c = conn.cursor()
    c.execute("DELETE FROM gastos WHERE user_id = ? AND categoria = ?", (user_id, categoria))
    conn.commit()
    conn.close()

