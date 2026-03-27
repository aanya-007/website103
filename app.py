from flask import Flask, render_template, request
import pg8000.native
import os
import urllib.parse

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    url = urllib.parse.urlparse(DATABASE_URL)
    return pg8000.native.Connection(
        host=url.hostname,
        port=url.port or 5432,
        database=url.path.lstrip("/"),
        user=url.username,
        password=url.password,
        ssl_context=True
    )

def init_db():
    conn = get_conn()
    conn.run("""
        CREATE TABLE IF NOT EXISTS feedback (
            id      SERIAL PRIMARY KEY,
            name    TEXT NOT NULL,
            event   TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.close()

@app.route("/")
def index():
    try:
        init_db()
    except Exception as e:
        return f"<h2>DB Error:</h2><pre>{e}</pre>", 500
    return render_template("index.html", submitted=False)

@app.route("/submit", methods=["POST"])
def submit():
    name    = request.form.get("name",    "").strip()
    event   = request.form.get("event",   "").strip()
    message = request.form.get("message", "").strip()
    if not name or not event or not message:
        return render_template("index.html", submitted=False,
                               error="Please fill in all fields.")
    try:
        conn = get_conn()
        conn.run(
            "INSERT INTO feedback (name, event, message) VALUES (:name, :event, :message)",
            name=name, event=event, message=message
        )
        conn.close()
    except Exception as e:
        return f"<h2>Insert Error:</h2><pre>{e}</pre>", 500
    return render_template("index.html", submitted=True)
```

**4. Save** (Ctrl+S) and **close Notepad**

**5. Also open `requirements.txt` in Notepad** and make sure it contains exactly:
```
flask
pg8000