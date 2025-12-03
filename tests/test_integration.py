import pytest
from app.app import create_app
from app.extensions import db
from app.models import User, Task
from datetime import date

@pytest.fixture
def client():
    # Création de l'app en mode Test
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Désactive la protection CSRF pour les tests
    # Utilisation de SQLite en mémoire pour aller vite et ne pas toucher à Postgres
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register_flow(client):
    """Test inscription + redirection vers login."""
    response = client.post("/register", data={
        "username": "integration_user",
        "password": "password123",
        "confirm": "password123"  # Ton code demande ce champ 'confirm'
    }, follow_redirects=True)
    
    # Si tout va bien, on est redirigé vers login, ou on a un message de succès
    assert response.status_code == 200
    # Vérification en base
    with client.application.app_context():
        assert User.query.filter_by(username="integration_user").first() is not None

def test_create_task_flow(client):
    """Test : Inscription -> Login -> Création de tâche."""
    # 1. Inscription
    client.post("/register", data={
        "username": "task_user", "password": "123", "confirm": "123"
    }, follow_redirects=True)

    # 2. Login
    login_resp = client.post("/login", data={
        "username": "task_user", "password": "123"
    }, follow_redirects=True)
    assert b"Logged in successfully" in login_resp.data

    # 3. Création de tâche
    response = client.post("/tasks/new", data={
        "title": "Ma Tache Test",
        "description": "Ceci est un test",
        "due_date": str(date.today())
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Task created" in response.data
    
    # Vérification en base
    with client.application.app_context():
        task = Task.query.first()
        assert task.title == "Ma Tache Test"
        assert task.user.username == "task_user"
