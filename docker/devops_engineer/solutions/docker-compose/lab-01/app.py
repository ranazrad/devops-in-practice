from flask import Flask, jsonify, request
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

@app.route("/songs", methods=["GET"])
def get_songs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return jsonify(songs)

@app.route("/songs", methods=["POST"])
def add_song():
    data = request.json
    title = data.get("title")
    artist = data.get("artist")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (title, artist) VALUES (%s, %s)", (title, artist))
    conn.commit()
    conn.close()

    return jsonify({"message": "Song added!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
