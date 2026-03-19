from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

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
        data.get('name'), data.get('age'), data.get('location'), data.get('role'),
        data.get('skills'), data.get('email'), data.get('phone'), data.get('portfolio')
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Application submitted successfully!"})

@app.route('/data')
def data():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, age, location, role, skills, email, phone, portfolio FROM applications")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DHP Creations - Applications</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
            h1 { text-align: center; color: #2575fc; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
            th { background: #2575fc; color: white; }
            tr:nth-child(even) { background: #e6f0ff; }
            a { color: #2575fc; text-decoration: none; }
            .back-button { display:block; width:200px; margin: 30px auto; text-align:center; padding:12px; background:#2575fc; color:white; text-decoration:none; border-radius:8px; font-weight:bold; }
            .back-button:hover { background:#6a11cb; }
        </style>
    </head>
    <body>
        <h1>DHP Creations - Applications</h1>
        {% if rows %}
        <table>
            <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Location</th>
                <th>Role</th>
                <th>Skills</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Portfolio</th>
            </tr>
            {% for r in rows %}
            <tr>
                <td>{{ r[0] }}</td>
                <td>{{ r[1] }}</td>
                <td>{{ r[2] }}</td>
                <td>{{ r[3] }}</td>
                <td>{{ r[4] }}</td>
                <td>{{ r[5] }}</td>
                <td>{{ r[6] }}</td>
                <td>{% if r[7] %}<a href="{{ r[7] }}" target="_blank">Link</a>{% else %}-{% endif %}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p style="text-align:center; color:gray; font-size:1.2rem;">No submissions yet.</p>
        {% endif %}
        <a href="https://dhpcreations.netlify.app/" class="back-button">← Back to Home</a>
    </body>
    </html>
    """
    return render_template_string(html, rows=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)