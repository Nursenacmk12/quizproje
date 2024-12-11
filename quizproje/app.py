from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı oluşturma
def create_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS scores (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     score INTEGER NOT NULL)''')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    answer1 = request.form['q1']
    answer2 = request.form['q2']
    answer3 = request.form['q3']

    # Doğru cevaplar
    correct_answers = {"q1": "Blue", "q2": "Dog", "q3": "Python"}
    score = 0

    # Puan hesaplama
    if answer1 == correct_answers["q1"]:
        score += 1
    if answer2 == correct_answers["q2"]:
        score += 1
    if answer3 == correct_answers["q3"]:
        score += 1

    # Veritabanına kaydet
    conn = get_db_connection()
    conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

    return render_template('result.html', name=name, score=score)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
