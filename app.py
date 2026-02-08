from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# Database Model
# -------------------------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create DB
with app.app_context():
    db.create_all()

# -------------------------
# READ
# -------------------------
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# -------------------------
# CREATE
# -------------------------
@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['task']
    new_task = Todo(task=task_text)

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# -------------------------
# UPDATE
# -------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.task = request.form['task']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)

# -------------------------
# DELETE
# -------------------------
@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

# -------------------------
# COMPLETE FEATURE
# -------------------------
@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)

    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for('index'))

# -------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

