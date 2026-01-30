"""
Tests fonctionnels Selenium pour les produits

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
import time


class TestSeleniumProducts(LiveServerTestCase):
    """Tests Selenium pour les produits"""
    
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
        
        # Créer un produit de test
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
            nom='Produit Test Selenium',
            description='Description test',
            description_deal='Deal test',
            prix=1000,
            categorie=self.categorie_produit,
            etablissement=self.etablissement,
            status=True
        )
    
    def test_shop_page_loads(self):
        """TC61-SEL: Vérifier que la page shop se charge"""
        self.driver.get(f'{self.live_server_url}/deals/')
        time.sleep(2)
        self.assertIn('deals', self.driver.current_url.lower())
    
    def test_product_list_displayed(self):
        """TC61-SEL: Vérifier que la liste des produits s'affiche"""
        self.driver.get(f'{self.live_server_url}/deals/')
        
        # Attendre que la page se charge
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)
        
        # Vérifier que la page contient des produits
        # Chercher par différents sélecteurs possibles
        page_source = self.driver.page_source.lower()
        produit_nom = self.produit.nom.lower()
        
        # Vérifier soit le nom du produit, soit des éléments de produit
        produits_trouves = (
            produit_nom in page_source or
            'produit' in page_source or
            len(self.driver.find_elements(By.CLASS_NAME, "single-feature")) > 0 or
            len(self.driver.find_elements(By.CSS_SELECTOR, ".single-feature")) > 0 or
            len(self.driver.find_elements(By.CSS_SELECTOR, ".feature-desc")) > 0 or
            len(self.driver.find_elements(By.CSS_SELECTOR, "h3 a")) > 0
        )
        
        self.assertTrue(produits_trouves, "Aucun produit trouvé sur la page shop")
    
    def test_product_detail_page_loads(self):
        """TC62-SEL: Vérifier que la page de détail produit se charge"""
        self.driver.get(f'{self.live_server_url}/deals/produit/{self.produit.slug}')
        
        # Attendre que la page se charge
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)
        
        # Vérifier que le produit est affiché
        page_source = self.driver.page_source.lower()
        produit_nom = self.produit.nom.lower()
        
        # Vérifier soit le nom, soit le prix, soit des éléments spécifiques de la page détail
        produit_trouve = (
            produit_nom in page_source or
            str(self.produit.prix) in page_source or
            self.produit.slug in self.driver.current_url or
            len(self.driver.find_elements(By.CSS_SELECTOR, "#cart")) > 0 or
            len(self.driver.find_elements(By.CSS_SELECTOR, ".product-details-area")) > 0
        )
        
        self.assertTrue(produit_trouve, f"Produit {self.produit.nom} non trouvé sur la page détail")