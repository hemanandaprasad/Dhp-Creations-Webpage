from flask import Flask, request, jsonify, render_template_string, redirect
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Database URL from Render environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://dhp_creations_webpage_user:zpvA6GOp6ZZwq8z9jP7H124NhxpFfYnz@dpg-d6te41f5r7bs73abruv0-a.oregon-postgres.render.com/dhp_creations_webpage")

def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

# Health check route
@app.route("/ping")
def ping():
    return "Backend is live!"

# Redirect homepage to Netlify frontend
@app.route("/")
def home():
    return redirect("https://dhpcreations.netlify.app/")

# Submit route with confirmation page
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    conn = get_db()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
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
    
    # Return JSON if called via API
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({"message": "Application submitted successfully!"})
    
    # Return HTML confirmation page if opened in browser
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submission Successful</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align:center; padding:50px; background:#f5f5f5; }}
            h1 {{ color: #2575fc; }}
            p {{ font-size: 1.2rem; }}
            a {{ display:inline-block; margin-top:30px; padding:12px 20px; background:#2575fc; color:white; text-decoration:none; border-radius:8px; }}
            a:hover {{ background:#6a11cb; }}
        </style>
    </head>
    <body>
        <h1>Thank You, {data.get('name')}!</h1>
        <p>Your application has been submitted successfully.</p>
        <a href="https://dhpcreations.netlify.app/">← Back to Home</a>
    </body>
    </html>
    """
    return html

# Data page with pretty table and Back button
@app.route('/data')
def data():
    conn = get_db()
    if not conn:
        return "<p style='color:red;text-align:center;'>Database connection failed!</p>", 500
    
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