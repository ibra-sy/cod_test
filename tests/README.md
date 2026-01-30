# Suite de Tests - Application E-Commerce CoolDeal

## 📋 Vue d'ensemble

Cette suite de tests complète couvre l'application e-commerce CoolDeal développée avec Django.

**Statistiques :**
- **97 cas de test** couvrant les fonctionnalités critiques
- **4 types de tests** : unitaires, fonctionnels, intégration, performance
- **72 tests réussis** sur 97 (74.2% de taux de réussite)
- **83% de couverture de code** (2467 lignes testées)

## 📁 Structure

```
tests/
├── __init__.py
├── README.md                        # Ce fichier
├── RAPPORT_DE_TEST.md              # Rapport de test complet
├── unitaires/
│   ├── __init__.py
│   ├── test_models_produit.py     # TC01-TC05 : Tests modèle Produit
│   ├── test_models_panier.py      # TC06-TC10, TC19-TC20 : Tests Panier, CodePromo
│   ├── test_models_customer.py    # TC11-TC15 : Tests Customer, PasswordReset
│   ├── test_models_commande.py    # TC16-TC18 : Tests Commande
│   ├── test_models_favorite.py    # TC21-TC22 : Tests Favorite
│   ├── test_models_contact.py     # TC23-TC26 : Tests Contact, NewsLetter
│   └── test_models_etablissement.py # TC27-TC30 : Tests Etablissement
├── fonctionnels/
│   ├── __init__.py
│   ├── test_authentication.py      # TC31-TC46 : Tests d'authentification
│   ├── test_cart.py                # TC47-TC60 : Tests du panier
│   ├── test_products.py            # TC61-TC70 : Tests des produits
│   └── test_orders.py              # TC71-TC80 : Tests des commandes
├── integration/
│   ├── __init__.py
│   └── test_user_flow.py           # TC81-TC90 : Tests d'intégration
└── performance/
    ├── __init__.py
    └── test_performance.py         # TC91-TC97 : Tests de performance
```

## 🚀 Exécution des tests

### Prérequis

1. **Activer l'environnement virtuel** (venv) :

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

2. **Installer les dépendances** :

```bash
# Installer toutes les dépendances
pip install -r requirements.txt

# Ou installer les packages essentiels pour les tests
pip install Django django-cities-light django-daisy coverage
```

### Exécuter tous les tests

```bash
# Avec l'environnement virtuel activé
python manage.py test tests

# Ou directement avec le Python de venv
.\venv\Scripts\python.exe manage.py test tests
```

### Exécuter tous les tests avec détails

```bash
# Mode verbeux (recommandé)
python manage.py test tests --verbosity=2

# Mode très verbeux (maximum de détails)
python manage.py test tests --verbosity=3

# Sauvegarder les résultats dans un fichier
python manage.py test tests --verbosity=2 > test_results.txt
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

### Exécuter un fichier spécifique

```bash
# Tests des modèles produit
python manage.py test tests.unitaire.test_models_produit

# Tests des modèles panier
python manage.py test tests.unitaire.test_models_panier

# Tests d'authentification
python manage.py test tests.fonctionnels.test_authentication

# Tests du panier
python manage.py test tests.fonctionnels.test_cart

# Tests des produits
python manage.py test tests.fonctionnels.test_products

# Tests des commandes
python manage.py test tests.fonctionnels.test_orders

# Tests d'intégration
python manage.py test tests.integration.test_user_flow

# Tests de performance
python manage.py test tests.performance.test_performance
```

### Exécuter un test spécifique

```bash
# Format : tests.module.fichier.ClasseTest.nom_test
python manage.py test tests.unitaire.test_models_produit.TestProduitModel.test_produit_creation

# Exemple : test de connexion
python manage.py test tests.fonctionnels.test_authentication.TestLoginView.test_login_avec_username_valide
```

### Exécuter avec couverture de code

```bash
# Exécuter les tests avec couverture
.\venv\Scripts\python.exe -m coverage run --source='.' manage.py test tests

# Afficher le rapport de couverture
.\venv\Scripts\python.exe -m coverage report

# Générer un rapport HTML détaillé
.\venv\Scripts\python.exe -m coverage html

# Ouvrir le rapport HTML (Windows)
start htmlcov/index.html
```

### Exécuter uniquement les tests réussis

```bash
# Pour déboguer, exécuter un test spécifique qui échoue
python manage.py test tests.fonctionnels.test_authentication.TestSignupView.test_inscription_avec_donnees_valides --verbosity=2
```

## 🚀 Lancer le projet (Serveur de développement)

### Préparer la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser
```

### Lancer le serveur

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Le serveur sera accessible sur http://127.0.0.1:8000/

# Pour spécifier un port différent
python manage.py runserver 8080

# Pour rendre accessible depuis le réseau local
python manage.py runserver 0.0.0.0:8000
```

### Accéder à l'application

- **Page d'accueil** : http://127.0.0.1:8000/
- **Administration Django** : http://127.0.0.1:8000/admin/
- **API REST** : http://127.0.0.1:8000/api-auth/

### Arrêter le serveur

Appuyez sur `Ctrl+C` dans le terminal où le serveur tourne.

## 📊 Couverture de code

### Installation de Coverage

```bash
pip install coverage
```

### Exécuter avec couverture

```bash
# Exécuter les tests avec couverture
.\venv\Scripts\python.exe -m coverage run --source='.' manage.py test tests

# Afficher le rapport textuel
.\venv\Scripts\python.exe -m coverage report

# Afficher uniquement les fichiers non couverts
.\venv\Scripts\python.exe -m coverage report --skip-covered

# Générer un rapport HTML détaillé (dans htmlcov/)
.\venv\Scripts\python.exe -m coverage html

# Ouvrir le rapport HTML (Windows)
start htmlcov/index.html

# Ouvrir le rapport HTML (Linux/Mac)
xdg-open htmlcov/index.html
```

**Résultats actuels de couverture :**
- **Couverture globale : 83%** (2467 lignes, 425 non couvertes)
- **customer.models : 96%**
- **shop.models : 96%**
- **customer.views : 84%**
- **shop.views : 49%** (à améliorer)

## 🔍 Analyse statique du code

### Installation de Flake8

```bash
pip install flake8
```

### Exécuter Flake8

```bash
flake8 .
```

### Configuration recommandée

Créer un fichier `.flake8` à la racine du projet :

```ini
[flake8]
max-line-length = 120
exclude = 
    migrations,
    __pycache__,
    manage.py,
    venv,
    env,
    staticfiles
```

## 📈 IDs des tests

### Tests unitaires (TC01-TC30)
- **TC01-TC05** : Modèle Produit
- **TC06-TC10** : Modèle Panier
- **TC11-TC12** : Modèle Customer
- **TC13-TC15** : PasswordResetToken
- **TC16-TC18** : Modèle Commande
- **TC19-TC20** : CodePromotionnel
- **TC21-TC22** : Favorite
- **TC23-TC24** : Contact
- **TC25-TC26** : NewsLetter
- **TC27-TC30** : Etablissement

### Tests fonctionnels (TC31-TC80)
- **TC31-TC35** : Connexion
- **TC36-TC40** : Inscription
- **TC41-TC45** : Réinitialisation mot de passe
- **TC46** : Déconnexion
- **TC47-TC60** : Gestion panier
- **TC61-TC70** : Gestion produits
- **TC71-TC80** : Commandes et paiement

### Tests d'intégration (TC81-TC90)
- **TC81** : Flux complet d'achat
- **TC82** : Flux avec coupon
- **TC83-TC90** : Autres flux utilisateur

### Tests de performance (TC91-TC97)
- **TC91-TC92** : Performance vues
- **TC93** : Performance panier
- **TC94** : Opérations en masse
- **TC95** : Requêtes concurrentes
- **TC96-TC97** : Optimisations DB

## 🐛 Résolution de problèmes

### Erreur : "No module named 'tests'"

Assurez-vous d'être à la racine du projet Django et que le dossier `tests/` est au même niveau que `manage.py`.

### Erreur : "Database locked"

Cela peut arriver si plusieurs processus tentent d'accéder à la base de données SQLite en même temps. Fermez les autres processus ou utilisez PostgreSQL en développement.

### Tests très lents

Si les tests sont lents, vérifiez :
1. Utilisation de `select_related()` et `prefetch_related()` dans les requêtes
2. Nombre de fixtures créées dans `setUp()`
3. Performance de la machine

## 📝 Notes importantes

1. **Base de données de test** : Django crée automatiquement une base de données de test (SQLite en mémoire par défaut) qui est détruite après les tests.

2. **Isolation** : Chaque test est isolé et s'exécute dans une transaction séparée qui est annulée après le test.

3. **Fixtures** : Les données sont créées dans `setUp()` de chaque classe de test. Pas besoin de fixtures JSON pour ces tests.

4. **Tests de performance** : Les seuils de temps peuvent varier selon la machine. Ajustez-les si nécessaire.

5. **Résultats actuels** : 
   - 72 tests réussis sur 97 (74.2%)
   - 6 tests échoués (failures)
   - 11 tests avec erreurs (errors)
   - Temps d'exécution : ~111-140 secondes

6. **Problèmes connus** :
   - Certains tests échouent à cause de problèmes de gestion d'erreurs dans le code
   - Les tests de panier nécessitent une correction de la création de Session
   - Certains calculs de totaux avec promotions/coupons sont incorrects

## 📚 Documentation

Pour plus de détails, consultez :
- **RAPPORT_DE_TEST.md** : Rapport complet et académique
- **Documentation Django Testing** : https://docs.djangoproject.com/en/4.2/topics/testing/

## 🤝 Contribution

Pour ajouter de nouveaux tests :
1. Respectez la structure existante
2. Utilisez des IDs de test séquentiels (TC98, TC99, ...)
3. Ajoutez des docstrings claires
4. Mettez à jour le rapport de test si nécessaire

---

## 🔧 Commandes utiles supplémentaires

### Nettoyer les fichiers de test

```bash
# Supprimer les fichiers .pyc
find . -type d -name __pycache__ -exec rm -r {} +
# Ou sur Windows PowerShell
Get-ChildItem -Path . -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force

# Supprimer les fichiers de coverage
Remove-Item -Recurse -Force htmlcov
Remove-Item -Force .coverage
```

### Vérifier la structure des tests

```bash
# Lister tous les fichiers de test
Get-ChildItem -Path tests -Recurse -Filter test_*.py

# Compter le nombre de tests
python manage.py test tests --dry-run
```

### Exécuter les tests en parallèle (si disponible)

```bash
# Avec pytest (si installé)
pip install pytest pytest-django
pytest tests/ -v
```

---

**Dernière mise à jour :** Décembre 2024  
**Statistiques réelles :** 72/97 tests réussis (74.2%), 83% de couverture

