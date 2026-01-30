"""
Tests unitaires pour les modèles Contact, NewsLetter

ID de tests : TC23-TC26
"""

from django.test import TestCase

from contact.models import Contact, NewsLetter


class TestContactModel(TestCase):
    """Tests unitaires pour Contact"""
    
    def test_contact_creation(self):
        """TC23: Création d'un message de contact"""
        contact = Contact.objects.create(
            nom='John Doe',
            email='john@example.com',
            sujet='Question',
            message='Message de test',
            status=True
        )
        self.assertIsNotNone(contact.id)
        self.assertEqual(contact.nom, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')
    
    def test_contact_str_representation(self):
        """TC24: Représentation string d'un contact"""
        contact = Contact.objects.create(
            nom='Jane Doe',
            email='jane@example.com',
            sujet='Support',
            message='Message'
        )
        self.assertEqual(str(contact), 'Jane Doe')


class TestNewsLetterModel(TestCase):
    """Tests unitaires pour NewsLetter"""
    
    def test_newsletter_creation(self):
        """TC25: Inscription à la newsletter"""
        newsletter = NewsLetter.objects.create(
            email='subscriber@example.com',
            status=True
        )
        self.assertIsNotNone(newsletter.id)
        self.assertEqual(newsletter.email, 'subscriber@example.com')
    
    def test_newsletter_str_representation(self):
        """TC26: Représentation string d'une newsletter"""
        newsletter = NewsLetter.objects.create(
            email='test@example.com'
        )
        self.assertEqual(str(newsletter), 'test@example.com')

