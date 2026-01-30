"""
Tests unitaires pour le modèle Etablissement

ID de tests : TC27-TC30
"""

from django.test import TestCase
from django.contrib.auth.models import User

from shop.models import CategorieEtablissement, Etablissement


class TestEtablissementModel(TestCase):
    """Tests unitaires pour Etablissement"""
    
    def setUp(self):
        """Configuration initiale"""
        self.user = User.objects.create_user(
            username='etabuser',
            email='etab@example.com',
            password='testpass123'
        )
        self.categorie_etab = CategorieEtablissement.objects.create(
            nom='Restaurant',
            description='Catégorie test',
            status=True
        )
    
    def test_etablissement_creation(self):
        """TC27: Création d'un établissement"""
        etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Mon Restaurant',
            description='Description restaurant',
            logo='logo.jpg',
            couverture='couv.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='Pierre',
            prenoms_duresponsable='Dupont',
            adresse='456 Avenue Test',
            pays='CI',
            contact_1='0987654321',
            email='restaurant@example.com'
        )
        self.assertIsNotNone(etablissement.id)
        self.assertEqual(etablissement.nom, 'Mon Restaurant')
    
    def test_etablissement_slug_auto_generation(self):
        """TC28: Génération automatique du slug pour établissement"""
        etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Restaurant Elite',
            description='Test',
            logo='logo.jpg',
            couverture='couv.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='John',
            prenoms_duresponsable='Doe',
            adresse='123 Rue',
            pays='CI',
            contact_1='0123456789',
            email='test@example.com'
        )
        self.assertIsNotNone(etablissement.slug)
        self.assertIn('restaurant-elite', etablissement.slug)
    
    def test_etablissement_user_update_on_save(self):
        """TC29: Mise à jour automatique des infos User lors de la sauvegarde"""
        etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Restaurant Test',
            description='Test',
            logo='logo.jpg',
            couverture='couv.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='Marie',
            prenoms_duresponsable='Martin',
            adresse='123 Rue',
            pays='CI',
            contact_1='0123456789',
            email='marie@example.com'
        )
        # Vérifier que les infos User ont été mises à jour
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Marie')
        self.assertEqual(self.user.first_name, 'Martin')
        self.assertEqual(self.user.email, 'marie@example.com')
    
    def test_etablissement_one_to_one_user(self):
        """TC30: Relation OneToOne entre User et Etablissement"""
        etablissement = Etablissement.objects.create(
            user=self.user,
            nom='Restaurant Unique',
            description='Test',
            logo='logo.jpg',
            couverture='couv.jpg',
            categorie=self.categorie_etab,
            nom_du_responsable='John',
            prenoms_duresponsable='Doe',
            adresse='123 Rue',
            pays='CI',
            contact_1='0123456789',
            email='test@example.com'
        )
        self.assertEqual(self.user.etablissement, etablissement)

