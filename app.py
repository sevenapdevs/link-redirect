from flask import Flask, jsonify, redirect
import sqlite3
import random
import string

app = Flask(__name__)

def generate_rndm_link():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for _ in range(10))

@app.route("/create/<path:original_link>")
def gen_redirect_link(original_link):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                original_link TEXT,
                redirect_link TEXT
            )
        """)

        rndm_link = generate_rndm_link()

        cursor.execute(
            f"INSERT INTO links VALUES ('{original_link}', '{rndm_link}')"
        )

        conn.commit()

    return jsonify({"short_link": rndm_link})

@app.route("/<redirection_link>")
def redirect_link(redirection_link):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()

        result = cursor.execute(
            f"SELECT original_link FROM links WHERE redirect_link='{redirection_link}'"
        ).fetchone()

    if result:
        return jsonify({"original_link": f"{result}"})

    return "Not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
