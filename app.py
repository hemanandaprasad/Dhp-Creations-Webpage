from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = "PASTE_YOUR_RENDER_DB_URL_HERE"

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO applications 
        (name, age, location, role, skills, email, phone, portfolio)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['name'], data['age'], data['location'], data['role'],
        data['skills'], data['email'], data['phone'], data['portfolio']
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Saved"})

@app.route('/data')
def data():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name, age, location, role, skills FROM applications")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "name": r[0],
            "age": r[1],
            "location": r[2],
            "role": r[3],
            "skills": r[4]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run()