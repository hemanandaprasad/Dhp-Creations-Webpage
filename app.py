from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Database URL from Render environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

def get_db():
    return psycopg2.connect(DATABASE_URL)

# Homepage showing backend status
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DHP Creations Backend</title>
        <style>
            body { font-family: Arial, sans-serif; text-align:center; padding:50px; background:#f5f5f5; }
            h1 { color: #2575fc; }
            p { font-size: 1.2rem; }
        </style>
    </head>
    <body>
        <h1>DHP Creations Backend Running!</h1>
        <p>Use the frontend form on Netlify to submit applications.</p>
        <p>Click <a href="/data">here</a> to view submissions (currently empty).</p>
    </body>
    </html>
    """

# Submit route with confirmation
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

# View data page
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
            body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; text-align:center; }
            h1 { color: #2575fc; }
            table { width: 90%; margin: 20px auto; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
            th { background: #2575fc; color: white; }
            tr:nth-child(even) { background: #e6f0ff; }
            .back-button { display:block; width:200px; margin: 30px auto; text-align:center; padding:12px; background:#2575fc; color:white; text-decoration:none; border-radius:8px; font-weight:bold; }
            .back-button:hover { background:#6a11cb; }
        </style>
    </head>
    <body>
        <h1>DHP Creations - Applications</h1>
        {% if rows %}
        <table>
            <tr>
                <th>Name</th><th>Age</th><th>Location</th><th>Role</th>
                <th>Skills</th><th>Email</th><th>Phone</th><th>Portfolio</th>
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
        <p style="color:gray; font-size:1.2rem;">No submissions yet.</p>
        {% endif %}
        <a href="/" class="back-button">← Back to Backend Home</a>
    </body>
    </html>
    """
    return render_template_string(html, rows=rows)

# Route to clear all submissions
@app.route('/clear', methods=['POST'])
def clear():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM applications")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "All entries cleared!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)