# 🛒 Shopfront - Plateforme E-Commerce Django

**Shopfront** est une solution e-commerce complète développée en **Django 4.2**, proposant à la fois un site vitrine / boutique pour les clients et une interface de gestion avancée pour les administrateurs (tableaux de bord, graphiques analytiques Matplotlib, gestion des commandes, livraisons et notifications).

---

## ⚡ Démarrage Rapide en 1 Seule Commande (Docker)

Le projet est entièrement dockerisé. Toutes les étapes (installation des dépendances, création et application des migrations, collecte des fichiers statiques, démarrage du serveur Gunicorn) sont exécutées automatiquement lors du lancement du conteneur.

### Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) et **Docker Compose** installés.

### Commande de Lancement Unique

À la racine du dossier du projet (`SHOPFRONT`), exécutez simplement :

```bash
docker-compose up --build
```

L'application démarrera automatiquement et sera disponible sur le port **8000**.

---

## 🌐 Liens et Accès

Une fois l'application démarrée :

- **Boutique & Accueil Client** : [http://localhost:8000/](http://localhost:8000/)
- **Boutique Produits** : [http://localhost:8000/shop/](http://localhost:8000/shop/)
- **Tableau de Bord Administrateur (Custom)** : [http://localhost:8000/super/](http://localhost:8000/super/)
- **Administration Django Officielle** : [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔑 Créer un Super-Utilisateur / Administrateur

Pour vous connecter à l'espace d'administration (`/super/` ou `/admin/`), créez un compte administrateur avec la commande Docker suivante dans un nouveau terminal :

```bash
docker-compose exec web python manage.py createsuperuser
```

Suivez les instructions sur votre écran (Nom, Prénom, Nom d'utilisateur, Email, Mot de passe).

---

## 🛠️ Démarrage Local (Sans Docker)

Si vous préférez exécuter l'application localement sans Docker :

1. **Créer et activer un environnement virtuel** :
   ```bash
   python -m venv venv
   # Sur Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   # Sur Linux / macOS
   source venv/bin/activate
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations de base de données** :
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Lancer le serveur de développement** :
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

---

## 🏗️ Architecture & Technologies Utilisées

- **Back-end** : Python 3.10 / Django 4.2
- **Front-end** : HTML5, CSS3, JavaScript, Bootstrap 4/5
- **Formulaires & UI** : Django Crispy Forms (`crispy-bootstrap4`)
- **Analytique & Graphiques** : Matplotlib (Génération dynamique de graphiques en secteur et en barres)
- **Notification SMS** : Intégration Twilio (avec fallback sécurisé)
- **Serveur d'application** : Gunicorn
- **Conteneurisation** : Docker, Docker Compose
