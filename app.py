import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Get database URL from Render environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Create table automatically
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            marks INTEGER NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        marks = request.form["marks"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, roll, marks) VALUES (%s, %s, %s)",
            (name, roll, marks)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/view")

    return render_template("index.html")

@app.route("/view")
def view():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY id DESC;")
    students = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("view.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)