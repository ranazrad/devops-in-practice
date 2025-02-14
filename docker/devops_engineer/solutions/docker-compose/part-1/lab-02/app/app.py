from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.route("/")
def home():
    visits = cache.incr("counter")
    return f"Hello, Docker! This page has been visited {visits} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
