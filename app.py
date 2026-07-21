import json
import random
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


# ---------------- DATABASE ----------------

def create_database():

    conn = sqlite3.connect("chat_history.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


create_database()



# ---------------- LOAD INTENTS ----------------

with open("intents.json", encoding="utf-8") as file:

    intents = json.load(file)



# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    return render_template("index.html")



# ---------------- CHAT API ----------------

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"].lower()


    reply = "I'm sorry, I couldn't understand your request. Could you please rephrase it? 😊"



    # Search intent

    for intent in intents["intents"]:

        for pattern in intent["patterns"]:

            if pattern in user_message:

                reply = random.choice(intent["responses"])

                break


        if reply != "I'm sorry, I couldn't understand your request. Could you please rephrase it? 😊":

            break



    # Save chat history

    conn = sqlite3.connect("chat_history.db")

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO chats(user_message, bot_response, timestamp)
        VALUES (?, ?, ?)
        """,
        (
            user_message,
            reply,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )


    conn.commit()

    conn.close()



    return jsonify({

        "reply": reply

    })



# ---------------- CHAT HISTORY PAGE ----------------

@app.route("/history")
def history():

    conn = sqlite3.connect("chat_history.db")

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM chats ORDER BY id DESC"
    )


    chats = cursor.fetchall()


    conn.close()


    return render_template(
        "history.html",
        chats=chats
    )



# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)