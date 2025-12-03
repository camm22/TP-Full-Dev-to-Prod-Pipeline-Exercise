FROM python:3.12-slim

# 2. On définit le dossier de travail dans le conteneur
WORKDIR /app

# 3. On copie d'abord les dépendances (pour optimiser le cache Docker)
COPY requirements.txt .

# 4. Installation des dépendances
# --no-cache-dir permet de réduire la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout le reste du code de l'application
COPY . .

# 6. (Optionnel mais recommandé) On crée un utilisateur non-root pour la sécurité
RUN useradd -m appuser
USER appuser

# 7. On indique que l'app écoute sur le port 5000
EXPOSE 5000

# 8. Commande de démarrage en Production
# On utilise gunicorn au lieu de python app.py
# "app.app:create_app()" signifie : chercher le fichier "app.py" dans le dossier "app/" et la fonction "create_app()" dedans
# "-b 0.0.0.0:5000" rend l'app accessible depuis l'extérieur du conteneur
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.app:create_app()"]
