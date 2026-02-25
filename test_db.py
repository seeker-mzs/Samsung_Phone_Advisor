from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/samsung_db"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()
except Exception as e:
    print("Error:", e)