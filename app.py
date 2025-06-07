from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'todo.db'

def get_db_connection():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row  #カラム名でアクセスできるように設定
  return conn

@app.route('/')
def index():
  #タスク一覧を表示
  conn = get_db_connection()
  tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
  conn.close()
  return render_template('index.html', tasks = tasks)

@app.route('/add', methods = ['POST'])
def add():
  #新しいタスクを表示
  title = request.form.get('title', '').strip()
  if title:
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,)) #末尾にタプルを入れた
    conn.commit()
    conn.close()
  return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    """タスクの完了フラグを切り替え"""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        new_status = 0 if task['completed'] == 1 else 1
        conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    """タスクを削除"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)