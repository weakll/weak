import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='liuzhewei985211')
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS night_market CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.execute("CREATE USER IF NOT EXISTS 'night_market'@'localhost' IDENTIFIED BY 'nm2026pass'")
    cur.execute("GRANT ALL PRIVILEGES ON night_market.* TO 'night_market'@'localhost'")
    cur.execute("FLUSH PRIVILEGES")
    conn.close()
    print("SUCCESS: DB and user created")
except Exception as e:
    print(f"FAIL: {e}")
