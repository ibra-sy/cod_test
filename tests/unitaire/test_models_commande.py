"""
Tests unitaires pour le modèle Commande

ID de tests : TC16-TC18
"""

from django.test import TestCase
from django.contrib.auth.models import User

from customer.models import Customer, Commande


class TestCommandeModel(TestCase):
    """Tests unitaires pour le modèle Commande"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.customer = Customer.objects.create(
            user=self.user,
            adresse='123 Rue Test',
            contact_1='0123456789'
        )
    
    def test_commande_creation(self):
        """TC16: Création d'une commande"""
        commande = Commande.objects.create(
            customer=self.customer,
            prix_total=5000,
            transaction_id='TRX123456',
            status=True
        )
        self.assertIsNotNone(commande.id)
        self.assertEqual(commande.prix_total, 5000)
        self.assertEqual(commande.transaction_id, 'TRX123456')
    
    def test_commande_check_paiement(self):
        """TC17: Vérification statut de paiement (toujours True actuellement)"""
        commande = Commande.objects.create(
            customer=self.customer,
            prix_total=5000,
            status=True
        )
        # La méthode check_paiement retourne toujours True dans le code actuel
        self.assertTrue(commande.check_paiement)
    
    def test_commande_str_representation(self):
        """TC18: Représentation string d'une commande"""
        commande = Commande.objects.create(
            customer=self.customer,
            prix_total=5000
        )
        self.assertEqual(str(commande), 'commande')

