import os
import unittest
from datetime import date, timedelta
from app.models import User, Task
from app.app import _build_postgres_uri

class TestUnit(unittest.TestCase):

    def test_build_postgres_uri(self):
        """Test si l'URI est bien construite."""
        # On sauvegarde l'environnement actuel pour le restaurer après
        old_environ = os.environ.copy()
        
        try:
            # On simule des variables d'env
            os.environ["POSTGRES_USER"] = "unit_user"
            os.environ["POSTGRES_PASSWORD"] = "unit_pass"
            os.environ["POSTGRES_HOST"] = "unit_host"
            os.environ["POSTGRES_PORT"] = "5432"
            os.environ["POSTGRES_DB"] = "unit_db"
            
            # Important : on supprime DATABASE_URL si elle existe pour forcer la construction manuelle
            if "DATABASE_URL" in os.environ:
                del os.environ["DATABASE_URL"]

            expected = "postgresql+psycopg2://unit_user:unit_pass@unit_host:5432/unit_db"
            self.assertEqual(_build_postgres_uri(), expected)
        
        finally:
            # Nettoyage : on remet l'environnement comme avant
            os.environ.clear()
            os.environ.update(old_environ)

    def test_user_password(self):
        """Test le hashage du mot de passe User."""
        u = User(username="test_unit")
        u.set_password("secret")
        
        self.assertNotEqual(u.password_hash, "secret")
        self.assertTrue(u.check_password("secret"))
        self.assertFalse(u.check_password("wrong"))

    def test_task_is_overdue(self):
        """Test la méthode is_overdue du modèle Task."""
        # Cas 1 : Tâche en retard (date d'hier)
        yesterday = date.today() - timedelta(days=1)
        t_overdue = Task(title="Retard", due_date=yesterday, is_completed=False)
        self.assertTrue(t_overdue.is_overdue())

        # Cas 2 : Tâche future (demain)
        tomorrow = date.today() + timedelta(days=1)
        t_future = Task(title="Futur", due_date=tomorrow, is_completed=False)
        self.assertFalse(t_future.is_overdue())

        # Cas 3 : Tâche terminée (même si date passée, elle n'est pas 'overdue')
        t_done = Task(title="Fini", due_date=yesterday, is_completed=True)
        self.assertFalse(t_done.is_overdue())
