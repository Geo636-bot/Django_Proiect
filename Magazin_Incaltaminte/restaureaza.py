import sqlite3

# Ne conectăm la baza de date
con = sqlite3.connect('db.sqlite3')
cursor = con.cursor()

print("Incepem restaurarea datelor...")

# Deschidem fisierul de backup si executam continutul
with open('backup_insert.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()
    cursor.executescript(sql_script)

# Salvam modificarile si inchidem conexiunea
con.commit()
con.close()

print("Restaurarea a fost finalizata cu succes!")