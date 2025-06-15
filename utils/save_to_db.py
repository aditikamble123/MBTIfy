import mysql.connector

def save_result_to_db(name, mbti_type):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aditikamble@2",
            database="mbti"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO results (name, mbti_type) VALUES (%s, %s)", (name, mbti_type))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB Error:", e)
from utils.save_to_db import save_result_to_db  # optional if using DB