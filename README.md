# prosody2ejabberdSqlMamMigrator
Migriert die MAM Nachrichten von Prosody nach Ejabberd, beide müssen mit Mysql laufen.


Es wird das Paket python3-mysql.connector gebraucht.

###Installation unter Ubuntu und Debian:

```bash
apt install python3-mysql.connector
```

###Einfach Zugangsdaten und Datenbank im Skript anpassen, ausführbar machen und ausführen:

```bash
./migrator.py
```