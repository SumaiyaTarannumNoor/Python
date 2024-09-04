from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# MySQL connection settings
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = db.cursor()

    if request.method == 'POST':
        message = request.form['message']
        cursor.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
        db.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT content FROM messages")
    messages = cursor.fetchall()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
