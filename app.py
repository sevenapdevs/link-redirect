from flask import Flask, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

@app.route("/create/<original_link>")
def gen_redirect_link(original_link):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS links (
            original_link TEXT,
            redirect_link TEXT
        )
"""
        cursor.execute(sql)

        # Generate redirection link
        rndm_link = generate_rndm_link()

        sql = f"""INSERT INTO links (original_link, redirect_link)
        VALUES ({original_link}, {rndm_link})
"""
        cursor.execute(sql)

    return jsonify({"result": "success"})

@app.route("/<redirection_link>")
def redirect(redirection_link):
    with sqlite3.connect("links.db") as conn:
        cursor = conn.cursor()
        sql = f"SELECT original_link FROM links WHERE redirect_link={redirection_link}"
        sql_result = cursor.execute(sql)
        fetch_result = sql_result.fetchall()
    return fetch_result
    
        
def generate_rndm_link():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for _ in range(10))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
