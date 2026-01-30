"""
Tests fonctionnels pour la gestion des produits

ID de tests : TC61-TC70
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement, Favorite
from customer.models import Customer


class TestProductViews(TestCase):
    """TC61-TC70: Tests fonctionnels pour les vues produits"""
    
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
        # Créer un établissement
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
            nom='Produit Test',
            description='Description test',
            description_deal='Deal test',
            prix=1000,
            quantite=10,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_shop_view_liste_produits(self):
        """TC61: Affichage de la liste des produits"""
        url = reverse('shop')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('produits', response.context)
        self.assertGreaterEqual(len(response.context['produits']), 1)
    
    def test_product_detail_view(self):
        """TC62: Affichage des détails d'un produit"""
        url = reverse('product_detail', args=[self.produit.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['produit'], self.produit)
    
    def test_product_detail_produit_inexistant(self):
        """TC63: Échec affichage produit inexistant"""
        url = reverse('product_detail', args=['produit-inexistant-123'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_toggle_favorite_add(self):
        """TC64: Ajout d'un produit aux favoris"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('toggle_favorite', args=[self.produit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Vérifier que le favori a été créé
        self.assertTrue(Favorite.objects.filter(user=self.user, produit=self.produit).exists())
    
    def test_toggle_favorite_remove(self):
        """TC65: Retrait d'un produit des favoris"""
        self.client.login(username='testuser', password='testpass123')
        # Ajouter d'abord aux favoris
        Favorite.objects.create(user=self.user, produit=self.produit)
        url = reverse('toggle_favorite', args=[self.produit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # Vérifier que le favori a été supprimé
        self.assertFalse(Favorite.objects.filter(user=self.user, produit=self.produit).exists())
    
    def test_toggle_favorite_requires_login(self):
        """TC66: Toggle favori requiert connexion"""
        url = reverse('toggle_favorite', args=[self.produit.id])
        response = self.client.get(url)
        # Devrait rediriger vers login (l'URL nommée 'login' pointe vers '/customer/')
        self.assertEqual(response.status_code, 302)
        # Le décorateur @login_required redirige vers '/customer/' selon customer/urls.py
        self.assertTrue('/customer/' in response.url or 'login' in response.url.lower())
    
    def test_categorie_view_liste_produits(self):
        """TC67: Affichage produits par catégorie"""
        url = reverse('categorie', args=[self.categorie_produit.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('produits', response.context)
        self.assertIn(self.produit, response.context['produits'])
    
    def test_categorie_etablissement_view(self):
        """TC68: Affichage produits par catégorie établissement"""
        url = reverse('categorie', args=[self.categorie_etab.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('produits', response.context)
    
    def test_product_detail_shows_favorite_status(self):
        """TC69: Détails produit affichent statut favori"""
        self.client.login(username='testuser', password='testpass123')
        # Ajouter aux favoris
        Favorite.objects.create(user=self.user, produit=self.produit)
        url = reverse('product_detail', args=[self.produit.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_favorited'])
    
    def test_shop_view_filters_status_active(self):
        """TC70: Liste produits filtre uniquement produits actifs"""
        # Créer un produit inactif
        produit_inactif = Produit.objects.create(
            nom='Produit Inactif',
            description='Test',
            description_deal='Deal',
            prix=2000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=False  # Inactif
        )
        url = reverse('shop')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        produits = response.context['produits']
        # Vérifier que le produit inactif n'est pas dans la liste
        self.assertNotIn(produit_inactif, produits)
        # Mais le produit actif devrait être présent
        self.assertIn(self.produit, produits)

