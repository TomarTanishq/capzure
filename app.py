from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tanishqtomar'

def get_db_connection():
    conn = sql.connect("students.db")
    conn.row_factory = sql.Row
    return conn

with get_db_connection() as connection:
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS student")
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS student (
                       fname TEXT, 
                       lname TEXT, 
                       id INTEGER PRIMARY KEY,
                       date_created TIMESTAMP,
                       image BLOB);
                   ''')
    connection.commit()

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    studentData = cursor.execute("SELECT * FROM student").fetchall()
    connection.close()
    return render_template('index.html', studentData=studentData)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        id = request.form['id']
        image = request.form['image']

        if not fname or not lname:
            flash('Name is required!')
        elif not id:
            flash('Student ID is required!')
        else:
            now=datetime.now()
            currentDateTime=now.strftime("%Y-%m-%d %H:%M")
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO student (fname, lname, id, date_created, image) VALUES (?, ?, ?, ?, ?)", (fname, lname, id, currentDateTime, image))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)
