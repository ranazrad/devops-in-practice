from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "host": "db_mysql",  # Matches the service name in docker-compose
    "user": "root",
    "password": "",
    "database": "music"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return render_template("index.html", songs=songs)

@app.route("/songs", methods=["POST"])
def add_song():
    title = request.form["title"]
    artist = request.form["artist"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (title, artist) VALUES (%s, %s)", (title, artist))
    conn.commit()
    conn.close()

    return jsonify({"title": title, "artist": artist})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
