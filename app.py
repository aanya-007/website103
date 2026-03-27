# app.py - Main Flask application file

# Import required libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Create the Flask app
app = Flask(__name__)

# Name of the SQLite database file
DATABASE = "feedback.db"


def init_db():
    """Create the database and feedback table if they don't exist yet."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            event   TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ── Route 1: Show the feedback form ──────────────────────────────────────────
@app.route("/")
def index():
    """Display the main feedback form page."""
    return render_template("index.html", submitted=False)


# ── Route 2: Handle form submission ──────────────────────────────────────────
@app.route("/submit", methods=["POST"])
def submit():
    """Receive form data, save it to SQLite, then show a success message."""

    # Read the values the student typed in the form
    name    = request.form.get("name",    "").strip()
    event   = request.form.get("event",   "").strip()
    message = request.form.get("message", "").strip()

    # Basic check: make sure none of the fields are empty
    if not name or not event or not message:
        return render_template("index.html", submitted=False,
                               error="Please fill in all fields.")

    # Save the feedback into the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (name, event, message) VALUES (?, ?, ?)",
        (name, event, message)
    )
    conn.commit()
    conn.close()

    # Re-render the same page with a success flag
    return render_template("index.html", submitted=True)


# ── Start the app ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()          # Make sure the database/table exist before starting
    app.run(debug=True)
