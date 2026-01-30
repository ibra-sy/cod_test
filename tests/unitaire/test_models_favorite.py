"""
Tests unitaires pour le modèle Favorite

ID de tests : TC21-TC22
"""

from django.test import TestCase
from django.contrib.auth.models import User

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement, Favorite


class TestFavoriteModel(TestCase):
    """Tests unitaires pour Favorite"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
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
        self.produit = Produit.objects.create(
            nom='Produit Favori',
            description='Test',
            description_deal='Deal',
            prix=1000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_favorite_creation(self):
        """TC21: Ajout d'un produit aux favoris"""
        favorite = Favorite.objects.create(
            user=self.user,
            produit=self.produit
        )
        self.assertIsNotNone(favorite.id)
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.produit, self.produit)
    
    def test_favorite_unique_together(self):
        """TC22: Unicité du couple user-produit"""
        Favorite.objects.create(
            user=self.user,
            produit=self.produit
        )
        # Tentative de créer un doublon doit échouer
        with self.assertRaises(Exception):  # IntegrityError
            Favorite.objects.create(
                user=self.user,
                produit=self.produit
            )

