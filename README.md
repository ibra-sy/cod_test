# CoolDeal - Plateforme E-Commerce Django

CoolDeal est une plateforme e-commerce complète développée avec Django 4.2.9, permettant la vente de produits et services (deals) par des établissements. L'application offre une expérience d'achat complète avec gestion de panier, codes promotionnels, système de favoris, et intégration de paiement.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Structure du projet](#-structure-du-projet)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement de l&#39;application](#-lancement-de-lapplication)
- [Exécution des tests](#-exécution-des-tests)
- [Documentation](#-documentation)

## ✨ Fonctionnalités

### Pour les clients

- **Authentification complète** : Inscription, connexion, réinitialisation de mot de passe
- **Catalogue de produits** : Navigation par catégories, recherche, filtrage
- **Gestion du panier** : Ajout, modification, suppression de produits
- **Codes promotionnels** : Application de coupons de réduction
- **Système de favoris** : Sauvegarde des produits préférés
- **Commandes** : Suivi des commandes, historique d'achats
- **Factures PDF** : Génération automatique de factures

### Pour les établissements

- **Dashboard** : Gestion des produits et commandes
- **Gestion produits** : Ajout, modification, suppression de produits
- **Promotions** : Gestion des promotions et prix promotionnels
- **Suivi des commandes** : Visualisation des commandes reçues

### Fonctionnalités générales

- **Interface responsive** : Design adaptatif pour tous les appareils
- **Paiement en ligne** : Intégration CinetPay
- **Newsletter** : Inscription à la newsletter
- **Formulaire de contact** : Communication avec le support

## 🛠 Technologies utilisées

- **Backend** : Django 4.2.9
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : HTML5, CSS3, JavaScript, Vue.js
- **Paiement** : CinetPay SDK
- **PDF** : xhtml2pdf, reportlab
- **Géolocalisation** : django-cities-light
- **API** : Django REST Framework, GraphQL (Graphene)
- **Tests** : Django TestCase, Selenium WebDriver
- **Déploiement** : Gunicorn, WhiteNoise

## 📁 Structure du projet

```
cooldeal/
├── base/                 # Application de base
├── client/              # Interface client (profil, commandes, favoris)
├── contact/             # Formulaire de contact et newsletter
├── cooldeal/            # Configuration principale Django
│   ├── settings.py     # Paramètres de l'application
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # Configuration WSGI
├── customer/            # Gestion clients, paniers, commandes, authentification
├── shop/                 # Gestion produits, catégories, établissements
├── website/             # Pages publiques et context processors
├── site_config/         # Configuration du site
├── tests/               # Suite complète de tests
│   ├── unitaire/       # Tests unitaires (30 tests)
│   ├── fonctionnels/   # Tests fonctionnels (50 tests + Selenium)
│   ├── integration/    # Tests d'intégration (10 tests)
│   └── performance/    # Tests de performance (7 tests)
├── media/               # Fichiers média uploadés
├── static/              # Fichiers statiques
├── staticfiles/         # Fichiers statiques collectés
├── manage.py            # Script de gestion Django
├── requirements.txt     # Dépendances Python
└── README.md           # Ce fichier
```

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le projet)

### Étapes d'installation

1. **Cloner le dépôt**

```bash
git clone <url-du-depot>
cd cod_test
```

2. **Créer un environnement virtuel**

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

3. **Activer l'environnement virtuel**

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

**Note** : Certains packages peuvent nécessiter des ajustements :

- `cinetpay-sdk` : Peut nécessiter une version spécifique ou un mock pour les tests
- `cities-light` : Installation standard via pip

5. **Appliquer les migrations**

```bash
python manage.py migrate
```

6. **Créer un superutilisateur (optionnel)**

```bash
python manage.py createsuperuser
```

## ⚙️ Configuration

### Variables d'environnement

Pour la production, configurez les variables suivantes dans `cooldeal/settings.py` ou via des variables d'environnement :

- `SECRET_KEY` : Clé secrète Django (à générer pour la production)
- `DEBUG` : `False` en production
- `ALLOWED_HOSTS` : Domaines autorisés
- `DATABASE_URL` : URL de la base de données (PostgreSQL recommandé en production)

### Configuration de la base de données

Par défaut, l'application utilise SQLite pour le développement. Pour la production, configurez PostgreSQL dans `settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cooldeal_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🎯 Lancement de l'application

### Mode développement

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1  # Windows
# ou
source venv/bin/activate     # Linux/Mac

# Lancer le serveur de développement
python manage.py runserver

# Le serveur sera accessible sur http://127.0.0.1:8000/
```

### Accès aux pages principales

- **Page d'accueil** : http://127.0.0.1:8000/
- **Boutique** : http://127.0.0.1:8000/deals/
- **Connexion** : http://127.0.0.1:8000/customer/
- **Inscription** : http://127.0.0.1:8000/customer/signup
- **Panier** : http://127.0.0.1:8000/deals/cart
- **Administration** : http://127.0.0.1:8000/admin/

### Mode production

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer avec Gunicorn
gunicorn cooldeal.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Exécution des tests

### Prérequis pour les tests

```bash
# Installer les dépendances de test
pip install coverage selenium webdriver-manager
```

### Exécuter tous les tests

```bash
# Avec l'environnement virtuel activé
python manage.py test tests

# Avec détails
python manage.py test tests --verbosity=2
```

### Exécuter par type de test

```bash
# Tests unitaires uniquement
python manage.py test tests.unitaire

# Tests fonctionnels uniquement
python manage.py test tests.fonctionnels

# Tests d'intégration uniquement
python manage.py test tests.integration

# Tests de performance uniquement
python manage.py test tests.performance
```

### Couverture de code

```bash
# Exécuter avec couverture
.\venv\Scripts\python.exe -m coverage run --source='.' manage.py test tests

# Afficher le rapport
.\venv\Scripts\python.exe -m coverage report

# Générer un rapport HTML
.\venv\Scripts\python.exe -m coverage html
start htmlcov/index.html  # Windows
```

### Statistiques des tests

- **Total** : 106 tests
- **Tests unitaires** : 30 tests (TC01-TC30)
- **Tests fonctionnels** : 50 tests (TC31-TC80)
- **Tests d'intégration** : 10 tests (TC81-TC90)
- **Tests de performance** : 7 tests (TC91-TC97)
- **Tests Selenium** : 9 tests (interface utilisateur)
- **Couverture de code** : 86%

Pour plus de détails sur les tests, consultez le [README des tests](tests/README.md).

## 📚 Documentation

### Documentation des tests

- **README des tests** : `tests/README.md` - Guide complet d'exécution des tests
- **Rapport de test** : `RAPPORT_DE_TEST_FINAL.docx` - Rapport académique complet

### Documentation Django

- [Documentation Django officielle](https://docs.djangoproject.com/)
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)

## 🔧 Commandes utiles

### Gestion de la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Gestion des fichiers statiques

```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Nettoyer les fichiers statiques collectés
python manage.py collectstatic --clear
```

### Shell Django

```bash
# Ouvrir le shell Django interactif
python manage.py shell
```

## 📊 Modules principaux

### customer

Gestion des clients, authentification, paniers, commandes, codes promotionnels, réinitialisation de mot de passe.

### shop

Gestion des produits, catégories, établissements, favoris, dashboard établissement.

### client

Interface client : profil, historique des commandes, favoris, paramètres.

### contact

Formulaire de contact et inscription à la newsletter.

### website

Pages publiques, context processors pour données globales (catégories, infos site).

## 🐛 Résolution de problèmes

### Erreur : "No module named 'cinetpay_sdk'"

Un mock minimal est fourni dans `customer/models.py`. Pour l'utilisation réelle, installez le SDK CinetPay.

### Erreur : "No module named 'django_daisy'"

```bash
pip install django-daisy
```

### Erreur : "Database locked"

Fermez les autres processus accédant à la base de données SQLite ou utilisez PostgreSQL.

### Tests Selenium échouent

Assurez-vous que Chrome/Chromium est installé. Le WebDriver sera téléchargé automatiquement via `webdriver-manager`.

## 📝 Notes importantes

- **Sécurité** : Changez `SECRET_KEY` en production
- **Base de données** : Utilisez PostgreSQL en production
- **Fichiers média** : Configurez un stockage approprié (S3, etc.) en production
- **Emails** : Configurez un backend email en production (SMTP, SendGrid, etc.)

## 👥 Contribution

Pour contribuer au projet :

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est un projet académique. Consultez les fichiers de licence pour plus d'informations.

## 👤 Auteur

**SYLLA SCHEICKNA IBRAHIM**

## 🙏 Remerciements

- Django pour le framework
- Tous les contributeurs des packages utilisés
- La communauté Django

---
