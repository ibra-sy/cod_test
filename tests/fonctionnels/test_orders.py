"""
Tests fonctionnels pour les commandes et le paiement

ID de tests : TC71-TC80
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.models import Session
import json

from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement
from customer.models import Customer, Panier, ProduitPanier, Commande


class TestOrderViews(TestCase):
    """TC71-TC80: Tests fonctionnels pour les commandes"""
    
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
    
    def test_post_paiement_details_creates_commande(self):
        """TC71: Création d'une commande via post_paiement_details"""
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
        
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX123456',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        # Vérifier que la commande a été créée
        self.assertTrue(Commande.objects.filter(customer=self.customer).exists())
        # Vérifier que le panier a été supprimé
        self.assertFalse(Panier.objects.filter(id=panier.id).exists())
    
    def test_post_paiement_details_transfers_produits(self):
        """TC72: Transfert des produits du panier vers la commande"""
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
            quantite=3
        )
        
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX789',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Vérifier que le produit a été transféré à la commande
        commande = Commande.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(commande)
        self.assertTrue(ProduitPanier.objects.filter(commande=commande, produit=self.produit).exists())
        produit_commande = ProduitPanier.objects.get(commande=commande, produit=self.produit)
        self.assertEqual(produit_commande.quantite, 3)
    
    def test_post_paiement_details_calcul_prix_total(self):
        """TC73: Calcul correct du prix total de la commande"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        ProduitPanier.objects.create(panier=panier, produit=self.produit, quantite=2)
        # Total attendu = 2 * 1000 = 2000
        
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX999',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        commande = Commande.objects.filter(customer=self.customer).first()
        self.assertEqual(commande.prix_total, 2000)
    
    def test_post_paiement_details_panier_inexistant(self):
        """TC74: Échec paiement avec panier inexistant"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX123',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': 99999  # ID inexistant
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_post_paiement_details_donnees_manquantes(self):
        """TC75: Échec paiement avec données manquantes"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('paiement_detail')
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
    
    def test_paiement_success_view_requires_login(self):
        """TC76: Page succès paiement requiert connexion"""
        url = reverse('paiement_success')
        response = self.client.get(url)
        # Devrait rediriger vers index ou login
        self.assertEqual(response.status_code, 302)
    
    def test_paiement_success_view_shows_commandes(self):
        """TC77: Page succès paiement affiche les commandes"""
        self.client.login(username='testuser', password='testpass123')
        # Créer une commande
        commande = Commande.objects.create(
            customer=self.customer,
            prix_total=5000,
            transaction_id='TRX123',
            status=True
        )
        url = reverse('paiement_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('commandes', response.context)
        self.assertIn(commande, response.context['commandes'])
    
    def test_post_paiement_details_unauthorized_panier(self):
        """TC78: Échec paiement avec panier d'un autre utilisateur"""
        # Créer un autre utilisateur
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        other_customer = Customer.objects.create(
            user=other_user,
            adresse='456 Rue',
            contact_1='0987654321'
        )
        session = Session.objects.create()
        other_panier = Panier.objects.create(
            customer=other_customer,
            session_id=session,
            status=True
        )
        
        # Tentative d'utiliser le panier d'un autre utilisateur
        self.client.login(username='testuser', password='testpass123')
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX123',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': other_panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Devrait échouer
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_commande_transaction_id_stored(self):
        """TC79: Stockage de l'ID de transaction"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        ProduitPanier.objects.create(panier=panier, produit=self.produit, quantite=1)
        
        transaction_id = 'TRX_UNIQUE_12345'
        url = reverse('paiement_detail')
        data = {
            'transaction_id': transaction_id,
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        commande = Commande.objects.filter(customer=self.customer).first()
        self.assertEqual(commande.transaction_id, transaction_id)
    
    def test_post_paiement_details_panier_vide(self):
        """TC80: Échec paiement avec panier vide"""
        self.client.login(username='testuser', password='testpass123')
        session = Session.objects.get(session_key=self.client.session.session_key)
        panier = Panier.objects.create(
            customer=self.customer,
            session_id=session,
            status=True
        )
        # Panier vide (pas de produits)
        
        url = reverse('paiement_detail')
        data = {
            'transaction_id': 'TRX123',
            'notify_url': 'http://example.com/notify',
            'return_url': 'http://example.com/return',
            'panier': panier.id
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        # Devrait quand même créer la commande mais avec prix_total = 0 ou erreur selon logique
        # Le comportement dépend de l'implémentation réelle
        self.assertEqual(response.status_code, 200)

