"""
Tests unitaires pour les modèles Panier, ProduitPanier, CodePromotionnel

ID de tests : TC06-TC10, TC19-TC20
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import date, timedelta

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement
from customer.models import Customer, Panier, ProduitPanier, CodePromotionnel


class TestPanierModel(TestCase):
    """Tests unitaires pour le modèle Panier"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.customer = Customer.objects.create(
            user=self.user,
            adresse='123 Rue Test',
            contact_1='0123456789'
        )
        # Créer une session valide avec expire_date
        from django.utils import timezone
        from datetime import timedelta
        session_key = 'test_session_key_12345'
        expire_date = timezone.now() + timedelta(days=1)
        self.session = Session.objects.create(
            session_key=session_key,
            expire_date=expire_date
        )
        self.panier = Panier.objects.create(
            customer=self.customer,
            session_id=self.session,
            status=True
        )
        # Créer un produit
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
            description='Test',
            description_deal='Deal',
            prix=1000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_panier_total_calcul(self):
        """TC06: Calcul du total du panier avec produits"""
        ProduitPanier.objects.create(
            produit=self.produit,
            panier=self.panier,
            quantite=2
        )
        # Total = 2 * 1000 = 2000
        self.assertEqual(self.panier.total, 2000)
    
    def test_panier_total_avec_coupon(self):
        """TC07: Calcul du total avec code promotionnel"""
        ProduitPanier.objects.create(
            produit=self.produit,
            panier=self.panier,
            quantite=2
        )
        coupon = CodePromotionnel.objects.create(
            libelle='Promo 10%',
            etat=True,
            date_fin=date.today() + timedelta(days=30),
            reduction=0.10,
            code_promo='PROMO10'
        )
        self.panier.coupon = coupon
        self.panier.save()
        # Total = 2000, réduction = 0.10 * 2000 = 200, total_with_coupon = 1800
        self.assertEqual(self.panier.total_with_coupon, 1800)
    
    def test_panier_check_empty_avec_produits(self):
        """TC08: Vérification panier non vide"""
        ProduitPanier.objects.create(
            produit=self.produit,
            panier=self.panier,
            quantite=1
        )
        self.assertTrue(self.panier.check_empty)
    
    def test_panier_check_empty_sans_produits(self):
        """TC09: Vérification panier vide"""
        self.assertFalse(self.panier.check_empty)
    
    def test_produit_panier_total_avec_promotion(self):
        """TC10: Calcul total ProduitPanier avec promotion active"""
        aujourdhui = date.today()
        self.produit.prix_promotionnel = 800
        self.produit.date_debut_promo = aujourdhui - timedelta(days=1)
        self.produit.date_fin_promo = aujourdhui + timedelta(days=7)
        self.produit.save()
        
        produit_panier = ProduitPanier.objects.create(
            produit=self.produit,
            panier=self.panier,
            quantite=3
        )
        # Total avec promo = 3 * 800 = 2400
        self.assertEqual(produit_panier.total, 2400)


class TestCodePromotionnelModel(TestCase):
    """Tests unitaires pour CodePromotionnel"""
    
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
            nom='Produit Test',
            description='Test',
            description_deal='Deal',
            prix=1000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_code_promo_creation(self):
        """TC19: Création d'un code promotionnel"""
        code = CodePromotionnel.objects.create(
            libelle='Promo Noël',
            etat=True,
            date_fin=date.today() + timedelta(days=30),
            reduction=0.15,
            code_promo='NOEL2024'
        )
        self.assertIsNotNone(code.id)
        self.assertEqual(code.code_promo, 'NOEL2024')
        self.assertEqual(code.reduction, 0.15)
    
    def test_code_promo_avec_produits(self):
        """TC20: Code promotionnel avec produits associés"""
        code = CodePromotionnel.objects.create(
            libelle='Promo Produit',
            etat=True,
            date_fin=date.today() + timedelta(days=30),
            reduction=0.20,
            code_promo='PRODUIT20'
        )
        code.forfait.add(self.produit)
        self.assertIn(self.produit, code.forfait.all())

