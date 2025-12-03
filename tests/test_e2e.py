import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# Importations spécifiques pour Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# URL locale de ton app (doit être lancée dans un autre terminal !)
BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="module")
def driver():
    """Setup du driver Firefox (GeckoDriver)."""
    # Installe et configure automatiquement le driver Firefox
    service = FirefoxService(GeckoDriverManager().install())
    
    # Lance Firefox
    driver = webdriver.Firefox(service=service)
    
    # Attend max 10s si un élément n'est pas trouvé tout de suite
    driver.implicitly_wait(10)
    
    yield driver
    
    # Ferme le navigateur à la fin du test
    driver.quit()

def test_full_scenario(driver):
    """Scenario : Inscription -> Login -> Créer Tâche -> Vérifier affichage."""
    
    # Générer un user unique pour éviter les conflits
    unique_user = f"user_{int(time.time())}"
    
    # 1. Aller sur Register
    driver.get(f"{BASE_URL}/register")
    
    # Remplissage du formulaire
    driver.find_element(By.NAME, "username").send_keys(unique_user)
    driver.find_element(By.NAME, "password").send_keys("pass")
    # Ton modèle demande un champ confirm
    driver.find_element(By.NAME, "confirm").send_keys("pass")
    
    # Soumission
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # 2. Login (Redirection ou manuel)
    time.sleep(1) 
    
    # Si redirection vers Login, on se connecte
    driver.find_element(By.NAME, "username").send_keys(unique_user)
    driver.find_element(By.NAME, "password").send_keys("pass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # 3. Créer une nouvelle tâche
    driver.get(f"{BASE_URL}/tasks/new")
    
    driver.find_element(By.NAME, "title").send_keys("Tache Firefox E2E")
    driver.find_element(By.NAME, "description").send_keys("Test sur Firefox")
    # Date au format YYYY-MM-DD
    driver.find_element(By.NAME, "due_date").send_keys("2025-12-31")
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # 4. Vérifier que la tâche est sur la page d'accueil
    time.sleep(1)
    assert "Tache Firefox E2E" in driver.page_source
    assert "Test sur Firefox" in driver.page_source
