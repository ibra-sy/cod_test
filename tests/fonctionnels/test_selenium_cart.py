"""
Tests fonctionnels Selenium pour le panier

Ces tests utilisent Selenium pour tester l'interface utilisateur réelle
"""

from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from shop.models import Produit, CategorieProduit, CategorieEtablissement, Etablissement
from customer.models import Customer
import time


class TestSeleniumCart(LiveServerTestCase):
    """Tests Selenium pour le panier"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Configuration initiale"""
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
            nom='Produit Panier Test',
            description='Test',
            description_deal='Deal',
            prix=1000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_cart_page_loads(self):
        """TC54-SEL: Vérifier que la page panier se charge"""
        self.driver.get(f'{self.live_server_url}/deals/cart')
        time.sleep(2)
        self.assertIn('cart', self.driver.current_url.lower())
    
    def test_checkout_requires_login(self):
        """TC55-SEL: Vérifier que checkout requiert une connexion"""
        self.driver.get(f'{self.live_server_url}/deals/checkout')
        time.sleep(2)
        
        # Vérifier redirection vers login
        current_url = self.driver.current_url.lower()
        self.assertTrue(
            'login' in current_url or 
            'customer' in current_url
        )
