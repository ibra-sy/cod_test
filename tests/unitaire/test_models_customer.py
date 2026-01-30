"""
Tests unitaires pour les modèles Customer, PasswordResetToken

ID de tests : TC11-TC15
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

from customer.models import Customer, PasswordResetToken


class TestCustomerModel(TestCase):
    """Tests unitaires pour le modèle Customer"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_customer_creation(self):
        """TC11: Création d'un client"""
        customer = Customer.objects.create(
            user=self.user,
            adresse='123 Rue Test',
            contact_1='0123456789',
            pays='CI'
        )
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.contact_1, '0123456789')
    
    def test_customer_one_to_one_user(self):
        """TC12: Relation OneToOne entre User et Customer"""
        customer = Customer.objects.create(
            user=self.user,
            adresse='123 Rue Test',
            contact_1='0123456789'
        )
        self.assertEqual(self.user.customer, customer)


class TestPasswordResetTokenModel(TestCase):
    """Tests unitaires pour PasswordResetToken"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_token_creation(self):
        """TC13: Création d'un token de réinitialisation"""
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='test_token_123456789'
        )
        self.assertIsNotNone(token.id)
        self.assertEqual(token.user, self.user)
    
    def test_token_is_valid_fresh(self):
        """TC14: Vérification token valide (créé il y a moins d'1 heure)"""
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='test_token'
        )
        self.assertTrue(token.is_valid())
    
    def test_token_is_valid_expired(self):
        """TC15: Vérification token expiré (créé il y a plus d'1 heure)"""
        token = PasswordResetToken.objects.create(
            user=self.user,
            token='test_token'
        )
        # Simuler un token expiré en modifiant la date de création
        token.created_at = now() - timedelta(hours=2)
        token.save()
        self.assertFalse(token.is_valid())

