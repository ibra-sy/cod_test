"""
Tests unitaires pour les modèles Produit, CategorieProduit, CategorieEtablissement

ID de tests : TC01-TC05
"""

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement


class TestProduitModel(TestCase):
    """Tests unitaires pour le modèle Produit"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.categorie_etab = CategorieEtablissement.objects.create(
            nom='Restaurant',
            description='Catégorie de restaurant',
            status=True
        )
        self.etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Restaurant Test',
            description='Description test',
            logo='test_logo.jpg',
            couverture='test_couv.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='John',
            prenoms_duresponsable='Doe',
            adresse='123 Rue Test',
            pays='CI',
            contact_1='0123456789',
            email='test@example.com'
        )
        self.categorie_produit = CategorieProduit.objects.create(
            nom='Plat',
            description='Description plat',
            categorie=self.categorie_etab,
            status=True
        )
    
    def test_produit_creation(self):
        """TC01: Création d'un produit valide"""
        produit = Produit.objects.create(
            nom='Pizza Margherita',
            description='Pizza classique',
            description_deal='Pizza à prix réduit',
            prix=5000,
            prix_promotionnel=3500,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            quantite=10,
            status=True
        )
        self.assertIsNotNone(produit.id)
        self.assertEqual(produit.nom, 'Pizza Margherita')
        self.assertEqual(produit.prix, 5000)
        self.assertTrue(produit.status)
    
    def test_produit_slug_auto_generation(self):
        """TC02: Génération automatique du slug"""
        produit = Produit.objects.create(
            nom='Burger Classic',
            description='Burger test',
            description_deal='Deal burger',
            prix=3000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
        self.assertIsNotNone(produit.slug)
        self.assertIn('burger-classic', produit.slug)
    
    def test_produit_check_promotion_valide(self):
        """TC03: Vérification promotion valide (dates dans la période)"""
        aujourdhui = date.today()
        produit = Produit.objects.create(
            nom='Produit Promo',
            description='Test',
            description_deal='Deal',
            prix=5000,
            prix_promotionnel=3000,
            date_debut_promo=aujourdhui - timedelta(days=1),
            date_fin_promo=aujourdhui + timedelta(days=7),
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
        self.assertTrue(produit.check_promotion)
    
    def test_produit_check_promotion_expiree(self):
        """TC04: Vérification promotion expirée"""
        aujourdhui = date.today()
        produit = Produit.objects.create(
            nom='Produit Expiré',
            description='Test',
            description_deal='Deal',
            prix=5000,
            prix_promotionnel=3000,
            date_debut_promo=aujourdhui - timedelta(days=10),
            date_fin_promo=aujourdhui - timedelta(days=1),
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
        self.assertFalse(produit.check_promotion)
    
    def test_produit_check_promotion_sans_dates(self):
        """TC05: Vérification promotion sans dates (pas de promotion)"""
        produit = Produit.objects.create(
            nom='Produit Sans Promo',
            description='Test',
            description_deal='Deal',
            prix=5000,
            prix_promotionnel=3000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
        self.assertFalse(produit.check_promotion)

