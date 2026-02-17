@echo off
color 0A
echo ========================================================
echo   BACKUP BAZE DE DATE - GENERARE COMENZI INSERT
echo ========================================================
echo.
echo Se proceseaza baza de date db.sqlite3...

:: 1. Generam un fisier Python temporar pentru a citi in siguranta baza de date SQLite
echo import sqlite3 > temp_backup.py
echo con = sqlite3.connect('db.sqlite3') >> temp_backup.py
echo f = open('backup_insert.sql', 'w', encoding='utf-8') >> temp_backup.py
echo count = 0 >> temp_backup.py
echo for line in con.iterdump(): >> temp_backup.py
:: Cautam doar comenzile INSERT si doar tabelele aplicatiei noastre (excluzand tabelele default Django)
echo     if line.startswith('INSERT INTO') and 'catalog_produse_' in line.lower(): >> temp_backup.py
echo         f.write(line + '\n') >> temp_backup.py
echo         count += 1 >> temp_backup.py
echo f.close() >> temp_backup.py
echo print(f"S-au extras si salvat {count} comenzi INSERT.") >> temp_backup.py

:: 2. Rulam scriptul Python
python temp_backup.py

:: 3. Stergem fisierul temporar pentru a pastra curatenia in proiect
del temp_backup.py

echo.
echo Backup-ul a fost finalizat cu succes!
echo Te rog sa verifici fisierul generat: backup_insert.sql
echo.
pause