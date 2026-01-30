"""
Tests de performance pour l'application e-commerce

ID de tests : TC91-TC95
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
import time
import json

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement
from customer.models import Customer, Panier, ProduitPanier, Commande
from contact.models import Contact


class TestPerformance(TestCase):
    """TC91-TC95: Tests de performance"""
    
    def setUp(self):
        """Configuration initiale"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            adresse='123 Rue Test',
            contact_1='0123456789'
        )
        self.categorie_etab = CategorieEtablissement.objects.create(
            nom='Restaurant',
            description='Test',
            status=True
        )
        self.etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Restaurant Test',
            description='Test',
            logo='test.jpg',
            couverture='test.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='John',
            prenoms_duresponsable='Doe',
            adresse='123 Rue',
            pays='CI',
            contact_1='0123456789',
            email='test@example.com'
        )
        self.categorie_produit = CategorieProduit.objects.create(
            nom='Plat',
            description='Test',
            categorie=self.categorie_etab,
            status=True
        )
        # Créer plusieurs produits pour les tests de charge
        for i in range(50):
            Produit.objects.create(
                nom=f'Produit {i}',
                description='Test',
                description_deal='Deal',
                prix=1000 + i * 100,
                categorie=self.categorie_produit,
                etablissement=self.etablissement,
                status=True
            )
    
    def test_shop_view_performance(self):
        """TC91: Performance de la vue shop avec nombreux produits"""
        url = reverse('shop')
        
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertEqual(response.status_code, 200)
        # La vue devrait charger en moins de 1 seconde (à ajuster selon besoins)
        self.assertLess(execution_time, 1.0, f"Temps d'exécution trop long: {execution_time}s")
    
    def test_database_query_optimization(self):
        """TC92: Optimisation des requêtes base de données"""
        from django.db import connection
        from django.db import reset_queries
        
        reset_queries()
        url = reverse('shop')
        
        self.client.get(url)
        
        # Vérifier le nombre de requêtes (doit être raisonnable)
        num_queries = len(connection.queries)
        # Avec 50 produits, on devrait avoir un nombre raisonnable de requêtes
        # (idéalement moins de 10 avec select_related/prefetch_related)
        self.assertLess(num_queries, 20, f"Trop de requêtes: {num_queries}")
    
    def test_cart_operations_performance(self):
        """TC93: Performance des opérations sur le panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        # Ajouter plusieurs produits
        produits = Produit.objects.all()[:10]
        for produit in produits:
            ProduitPanier.objects.create(
                panier=panier,
                produit=produit,
                quantite=2
            )
        
        # Test de calcul du total
        start_time = time.time()
        total = panier.total
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertIsNotNone(total)
        # Le calcul devrait être rapide même avec plusieurs produits
        self.assertLess(execution_time, 0.5, f"Calcul trop lent: {execution_time}s")
    
    def test_bulk_operations_performance(self):
        """TC94: Performance des opérations en masse"""
        # Créer plusieurs commandes
        start_time = time.time()
        
        for i in range(20):
            commande = Commande.objects.create(
                customer=self.customer,
                prix_total=1000 + i * 100,
                transaction_id=f'TRX{i}',
                status=True
            )
            produit = Produit.objects.first()
            ProduitPanier.objects.create(
                commande=commande,
                produit=produit,
                quantite=1
            )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Vérifier que les commandes ont été créées
        self.assertEqual(Commande.objects.filter(customer=self.customer).count(), 20)
        # Les opérations en masse devraient être raisonnablement rapides
        self.assertLess(execution_time, 2.0, f"Création en masse trop lente: {execution_time}s")
    
    def test_concurrent_requests(self):
        """TC95: Gestion de requêtes concurrentes"""
        # Simuler plusieurs requêtes simultanées
        start_time = time.time()
        
        # Requête 1: Liste produits
        response1 = self.client.get(reverse('shop'))
        
        # Requête 2: Détail produit
        produit = Produit.objects.first()
        response2 = self.client.get(reverse('product_detail', args=[produit.slug]))
        
        # Requête 3: Panier
        response3 = self.client.get(reverse('cart'))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Vérifier que toutes les requêtes ont réussi
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        
        # Les requêtes concurrentes devraient être gérées rapidement
        self.assertLess(execution_time, 1.5, f"Requêtes concurrentes trop lentes: {execution_time}s")
    
    def test_pagination_performance(self):
        """TC96: Performance avec pagination (si implémentée)"""
        # Créer beaucoup de produits
        for i in range(100):
            Produit.objects.create(
                nom=f'Produit Pagination {i}',
                description='Test',
                description_deal='Deal',
                prix=1000,
                categorie=self.categorie_produit,
                etablissement=self.etablissement,
                status=True
            )
        
        url = reverse('shop')
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertEqual(response.status_code, 200)
        # Même avec pagination, la vue devrait être rapide (tolérance de 0.1s)
        self.assertLess(execution_time, 1.1, f"Pagination trop lente: {execution_time}s")
    
    def test_database_indexes_efficiency(self):
        """TC97: Efficacité des index de base de données"""
        from django.db import connection
        
        # Test de recherche avec index
        start_time = time.time()
        produits = Produit.objects.filter(status=True)[:10]
        list(produits)  # Forcer l'évaluation
        end_time = time.time()
        
        execution_time = end_time - start_time
        # Les requêtes avec index devraient être rapides
        self.assertLess(execution_time, 0.5, f"Recherche avec index trop lente: {execution_time}s")

