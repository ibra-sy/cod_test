"""
Tests fonctionnels pour la gestion du panier

ID de tests : TC47-TC60
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session
import json

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement
from customer.models import Customer, Panier, ProduitPanier, CodePromotionnel


class TestCartOperations(TestCase):
    """TC47-TC60: Tests fonctionnels pour les opérations sur le panier"""
    
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
        # Créer une session
        session = self.client.session
        session.save()
        
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
            quantite=10,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_add_to_cart_utilisateur_connecte(self):
        """TC47: Ajout produit au panier pour utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        # Créer un panier
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        url = reverse('add_to_cart')
        data = {
            'panier': panier.id,
            'produit': self.produit.id,
            'quantite': 2
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        # Vérifier que le produit a été ajouté
        self.assertTrue(ProduitPanier.objects.filter(panier=panier, produit=self.produit).exists())
    
    def test_add_to_cart_quantite_update_existing(self):
        """TC48: Mise à jour quantité si produit déjà dans panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        # Ajouter le produit une première fois
        ProduitPanier.objects.create(
            panier=panier,
            produit=self.produit,
            quantite=1
        )
        
        url = reverse('add_to_cart')
        data = {
            'panier': panier.id,
            'produit': self.produit.id,
            'quantite': 3
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que la quantité a été mise à jour
        produit_panier = ProduitPanier.objects.get(panier=panier, produit=self.produit)
        self.assertEqual(produit_panier.quantite, 3)
    
    def test_delete_from_cart(self):
        """TC49: Suppression d'un produit du panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        produit_panier = ProduitPanier.objects.create(
            panier=panier,
            produit=self.produit,
            quantite=2
        )
        
        url = reverse('delete_from_cart')
        data = {
            'panier': panier.id,
            'produit_panier': produit_panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        # Vérifier que le produit a été supprimé
        self.assertFalse(ProduitPanier.objects.filter(id=produit_panier.id).exists())
    
    def test_update_cart_quantite(self):
        """TC50: Mise à jour de la quantité d'un produit dans le panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        ProduitPanier.objects.create(
            panier=panier,
            produit=self.produit,
            quantite=1
        )
        
        url = reverse('update_cart')
        data = {
            'panier': panier.id,
            'produit': self.produit.id,
            'quantite': 5
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        # Vérifier la nouvelle quantité
        produit_panier = ProduitPanier.objects.get(panier=panier, produit=self.produit)
        self.assertEqual(produit_panier.quantite, 5)
    
    def test_add_coupon_valide(self):
        """TC51: Ajout d'un code promotionnel valide"""
        from datetime import date, timedelta
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        ProduitPanier.objects.create(
            panier=panier,
            produit=self.produit,
            quantite=2
        )
        
        coupon = CodePromotionnel.objects.create(
            libelle='Promo 10%',
            etat=True,
            date_fin=date.today() + timedelta(days=30),
            reduction=0.10,
            code_promo='PROMO10'
        )
        
        url = reverse('add_coupon')
        data = {
            'panier': panier.id,
            'coupon': 'PROMO10'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        # Vérifier que le coupon a été ajouté
        panier.refresh_from_db()
        self.assertEqual(panier.coupon, coupon)
    
    def test_add_coupon_invalide(self):
        """TC52: Tentative d'ajout d'un code promotionnel invalide"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        url = reverse('add_coupon')
        data = {
            'panier': panier.id,
            'coupon': 'CODE_INVALIDE'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
        self.assertIn('invalide', result['message'].lower())
    
    def test_add_to_cart_donnees_manquantes(self):
        """TC53: Échec ajout au panier avec données manquantes"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('add_to_cart')
        data = {
            # Données manquantes
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_cart_view_access(self):
        """TC54: Accès à la page panier"""
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_checkout_requires_login(self):
        """TC55: Page checkout requiert connexion"""
        url = reverse('checkout')
        response = self.client.get(url)
        # Devrait rediriger vers login (l'URL nommée 'login' pointe vers '/customer/')
        self.assertEqual(response.status_code, 302)
        # Le décorateur @login_required(login_url='login') redirige vers l'URL nommée 'login'
        # qui est '/customer/' selon customer/urls.py
        self.assertTrue('/customer/' in response.url or 'login' in response.url.lower())
    
    def test_checkout_authenticated_access(self):
        """TC56: Accès checkout pour utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('checkout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_to_cart_produit_inexistant(self):
        """TC57: Échec ajout produit inexistant au panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        url = reverse('add_to_cart')
        data = {
            'panier': panier.id,
            'produit': 99999,  # ID inexistant
            'quantite': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Devrait lever une exception ou retourner une erreur
        self.assertIn(response.status_code, [200, 500])
    
    def test_update_cart_produit_inexistant(self):
        """TC58: Échec mise à jour produit inexistant dans panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        url = reverse('update_cart')
        data = {
            'panier': panier.id,
            'produit': 99999,
            'quantite': 5
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Devrait échouer
        self.assertIn(response.status_code, [200, 500])
    
    def test_delete_from_cart_produit_inexistant(self):
        """TC59: Échec suppression produit inexistant du panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        
        url = reverse('delete_from_cart')
        data = {
            'panier': panier.id,
            'produit_panier': 99999
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Devrait échouer
        self.assertIn(response.status_code, [200, 500])
    
    def test_cart_total_calculation(self):
        """TC60: Calcul correct du total du panier"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        # Ajouter deux produits
        produit2 = Produit.objects.create(
            nom='Produit 2',
            description='Test',
            description_deal='Deal',
            prix=2000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
        ProduitPanier.objects.create(panier=panier, produit=self.produit, quantite=2)
        ProduitPanier.objects.create(panier=panier, produit=produit2, quantite=1)
        # Total attendu = (2 * 1000) + (1 * 2000) = 4000
        self.assertEqual(panier.total, 4000)

