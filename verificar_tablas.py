import sqlite3

conn = sqlite3.connect('nutribox.db')
cursor = conn.cursor()

# Obtener lista de tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()

print("=" * 50)
print("TABLAS CREADAS EN LA BASE DE DATOS:")
print("=" * 50)

for tabla in tablas:
    print(f"✓ {tabla[0]}")
    
    # Obtener columnas de cada tabla
    cursor.execute(f"PRAGMA table_info({tabla[0]})")
    columnas = cursor.fetchall()
    
    for col in columnas:
        tipo = col[2]
        nullable = "NULL" if col[3] == 0 else "NOT NULL"
        pk = " [PK]" if col[5] == 1 else ""
        print(f"    - {col[1]}: {tipo} {nullable}{pk}")
    print()

conn.close()

print("=" * 50)
print(f"TOTAL: {len(tablas)} tablas")
print("=" * 50)
