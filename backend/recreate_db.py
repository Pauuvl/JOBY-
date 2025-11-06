import psycopg

# Conectar a la base de datos por defecto 'postgres'
conn = psycopg.connect(
    dbname='postgres',
    user='postgres',
    password='12345',
    host='127.0.0.1',
    port='5432',
    autocommit=True  # Necesario para DROP/CREATE DATABASE
)

cur = conn.cursor()

print("� Cerrando conexiones activas a joby_db...")
cur.execute("""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'joby_db'
      AND pid <> pg_backend_pid();
""")

print("�🗑️  Eliminando base de datos joby_db...")
cur.execute("DROP DATABASE IF EXISTS joby_db;")

print("🆕 Creando base de datos joby_db...")
cur.execute("CREATE DATABASE joby_db;")

cur.close()
conn.close()

print("✅ Base de datos recreada exitosamente!")
