# TP-Full-Dev-to-Prod-Pipeline-Exercise

New TP Camille Bordes

Comment lancer les tests ?

 1.  **Assure-toi que ton venv est activé.**
 2.  **Lance le serveur** dans un premier terminal :
     ```powershell
     python app.py
     ```
 3.  **Lance les tests** dans un second terminal (à la racine du projet) :

     Pour tout lancer d'un coup :
     ```powershell
     pytest
     ```

     Ou fichier par fichier :
     ```powershell
     pytest tests/test_unit.py
     pytest tests/test_integration.py
     pytest tests/test_e2e.py
