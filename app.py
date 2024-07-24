from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT NOT NULL,
                  status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, 'in-progress'))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT status FROM tasks WHERE id=?", (id,))
    current_status = c.fetchone()[0]
    new_status = 'done' if current_status == 'in-progress' else 'in-progress'
    c.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)