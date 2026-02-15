from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------ MODEL ------------------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), default="General")
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String(200), nullable=True)


with app.app_context():
    db.create_all()


# ------------------ HELPER FUNCTIONS ------------------
def get_task_stats():
    todos = Todo.query.all()
    
    total = len(todos)
    completed = len([t for t in todos if t.completed])
    pending = total - completed
    
    overdue = len([
        t for t in todos
        if t.due_date and t.due_date < date.today() and not t.completed
    ])
    
    due_today = len([
        t for t in todos
        if t.due_date and t.due_date == date.today() and not t.completed
    ])
    
    week_end = date.today() + timedelta(days=7)
    due_this_week = len([
        t for t in todos
        if t.due_date and date.today() <= t.due_date <= week_end and not t.completed
    ])
    
    high_priority = len([t for t in todos if t.priority == "High" and not t.completed])
    medium_priority = len([t for t in todos if t.priority == "Medium" and not t.completed])
    low_priority = len([t for t in todos if t.priority == "Low" and not t.completed])
    
    category_stats = db.session.query(
        Todo.category, 
        func.count(Todo.id)
    ).filter(Todo.completed == False).group_by(Todo.category).all()
    
    completion_rate = int((completed / total) * 100) if total > 0 else 0
    
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_completions = Todo.query.filter(
        Todo.completed == True,
        Todo.completed_at >= week_ago
    ).count()
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'due_today': due_today,
        'due_this_week': due_this_week,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'category_stats': dict(category_stats),
        'completion_rate': completion_rate,
        'recent_completions': recent_completions
    }


def get_productivity_data():
    days = []
    completed_counts = []
    
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        
        count = Todo.query.filter(
            Todo.completed == True,
            Todo.completed_at >= day_start,
            Todo.completed_at <= day_end
        ).count()
        
        days.append(day.strftime('%a'))
        completed_counts.append(count)
    
    return {'days': days, 'counts': completed_counts}


# ------------------ ROUTES ------------------

@app.route("/")
def index():
    filter_category = request.args.get('category', 'all')
    filter_priority = request.args.get('priority', 'all')
    filter_status = request.args.get('status', 'all')
    search_query = request.args.get('search', '')
    
    query = Todo.query
    
    if filter_category != 'all':
        query = query.filter_by(category=filter_category)
    
    if filter_priority != 'all':
        query = query.filter_by(priority=filter_priority)
    
    if filter_status == 'completed':
        query = query.filter_by(completed=True)
    elif filter_status == 'pending':
        query = query.filter_by(completed=False)
    elif filter_status == 'overdue':
        query = query.filter(
            Todo.completed == False,
            Todo.due_date < date.today()
        )
    
    if search_query:
        query = query.filter(Todo.task.contains(search_query))
    
    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    todos = query.order_by(Todo.completed, Todo.due_date).all()
    todos.sort(key=lambda x: (x.completed, priority_order.get(x.priority, 4), x.due_date or date.max))
    
    stats = get_task_stats()
    productivity = get_productivity_data()
    
    categories = db.session.query(Todo.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template(
        "index.html",
        todos=todos,
        stats=stats,
        productivity=productivity,
        categories=categories,
        current_filters={
            'category': filter_category,
            'priority': filter_priority,
            'status': filter_status,
            'search': search_query
        },
        datetime=datetime
    )


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    description = request.form.get("description", "")
    category = request.form.get("category")
    priority = request.form.get("priority")
    due = request.form.get("due_date")
    tags = request.form.get("tags", "")

    due_date = datetime.strptime(due, "%Y-%m-%d").date() if due else None

    new_task = Todo(
        task=task,
        description=description,
        category=category,
        priority=priority,
        due_date=due_date,
        tags=tags
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/complete/<int:id>")
def complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    task.completed_at = datetime.utcnow() if task.completed else None
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.task = request.form.get("task")
        task.description = request.form.get("description", "")
        task.category = request.form.get("category")
        task.priority = request.form.get("priority")
        task.tags = request.form.get("tags", "")

        due = request.form.get("due_date")
        task.due_date = datetime.strptime(due, "%Y-%m-%d").date() if due else None

        db.session.commit()
        return redirect(url_for('index'))

    return render_template("edit.html", task=task, stats=get_task_stats())


@app.route("/api/stats")
def api_stats():
    stats = get_task_stats()
    productivity = get_productivity_data()
    return jsonify({
        'stats': stats,
        'productivity': productivity
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)