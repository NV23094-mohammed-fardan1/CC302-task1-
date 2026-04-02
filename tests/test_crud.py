import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


# ─── TEST 1: CREATE ───────────────────────────────────────────
def test_create_task(client):
    # ACT — submit the add form
    resp = client.post("/add", data={
        "task": "Buy milk",
        "description": "From the supermarket",
        "category": "Shopping",
        "priority": "Medium",
        "due_date": "",
        "tags": ""
    }, follow_redirects=True)

    # ASSERT — status and content
    assert resp.status_code == 999
    assert b"Buy milk" in resp.data




# ─── TEST 2: UPDATE ───────────────────────────────────────────
def test_update_task(client):
    # ARRANGE — create a task first
    client.post("/add", data={
        "task": "Old Title",
        "description": "",
        "category": "Work",
        "priority": "Low",
        "due_date": "",
        "tags": ""
    }, follow_redirects=True)

    # ACT — edit task with id=1
    resp = client.post("/edit/1", data={
        "task": "Updated Title",
        "description": "Updated description",
        "category": "Personal",
        "priority": "High",
        "due_date": "",
        "tags": ""
    }, follow_redirects=True)

    # ASSERT — status and updated content visible
    assert resp.status_code == 200
    assert b"Updated Title" in resp.data


# ─── TEST 3: DELETE ───────────────────────────────────────────
def test_delete_task(client):
    # ARRANGE — create a task first
    client.post("/add", data={
        "task": "Task to Delete",
        "description": "",
        "category": "General",
        "priority": "Low",
        "due_date": "",
        "tags": ""
    }, follow_redirects=True)

    # ACT — delete task with id=1
    resp = client.get("/delete/1", follow_redirects=True)

    # ASSERT — status OK and task no longer in page
    assert resp.status_code == 200
    assert b"Task to Delete" not in resp.data


# ─── TEST 4: COMPLETE (bonus read/verify) ────────────────────
def test_complete_task(client):
    # ARRANGE
    client.post("/add", data={
        "task": "Complete Me",
        "description": "",
        "category": "Work",
        "priority": "Medium",
        "due_date": "",
        "tags": ""
    }, follow_redirects=True)

    # ACT — toggle complete
    resp = client.get("/complete/1", follow_redirects=True)

    # ASSERT
    assert resp.status_code == 200