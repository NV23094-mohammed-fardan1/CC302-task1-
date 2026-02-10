from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------ MODEL ------------------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), default="General")
    priority = db.Column(db.String(20), default="Low")
    due_date = db.Column(db.Date, nullable=True)


with app.app_context():
    db.create_all()


# ------------------ HOME ------------------
@app.route("/")
def index():
    todos = Todo.query.all()

    total = len(todos)
    completed = len([t for t in todos if t.completed])
    pending = total - completed
    overdue = len([
        t for t in todos
        if t.due_date and t.due_date < date.today() and not t.completed
    ])

    completion_percent = int((completed / total) * 100) if total > 0 else 0

    return render_template(
        "index.html",
        todos=todos,
        total=total,
        completed=completed,
        pending=pending,
        overdue=overdue,
        completion_percent=completion_percent
    )


# ------------------ ADD ------------------
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    category = request.form["category"]
    priority = request.form["priority"]
    due = request.form["due_date"]

    due_date = datetime.strptime(due, "%Y-%m-%d").date() if due else None

    new_task = Todo(
        task=task,
        category=category,
        priority=priority,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect("/")


# ------------------ DELETE ------------------
@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


# ------------------ TOGGLE COMPLETE ------------------
@app.route("/complete/<int:id>")
def complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect("/")


# ------------------ EDIT ------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.task = request.form["task"]
        task.category = request.form["category"]
        task.priority = request.form["priority"]

        due = request.form["due_date"]
        task.due_date = datetime.strptime(due, "%Y-%m-%d").date() if due else None

        db.session.commit()
        return redirect("/")

    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
