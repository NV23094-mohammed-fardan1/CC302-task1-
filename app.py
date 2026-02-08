from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Home Page
@app.route('/')
def index():
    tasks = Todo.query.all()

    total = len(tasks)
    completed = len([t for t in tasks if t.completed])

    return render_template(
        'index.html',
        tasks=tasks,
        total=total,
        completed=completed
    )

# Add Task
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    new_task = Todo(task=task)

    db.session.add(new_task)
    db.session.commit()

    return redirect('/')

# Complete Task
@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed

    db.session.commit()
    return redirect('/')

# Delete Task
@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/')

# Edit Task
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    task = Todo.query.get_or_404(id)
    task.task = request.form['task']

    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0")
