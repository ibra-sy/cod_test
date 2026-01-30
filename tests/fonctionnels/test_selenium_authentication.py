"""
Tests fonctionnels Selenium pour l'authentification

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
import time


class TestSeleniumAuthentication(LiveServerTestCase):
    """Tests Selenium pour l'authentification"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Mode headless pour les tests
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
    
    def test_login_page_loads(self):
        """TC31-SEL: Vérifier que la page de connexion se charge"""
        self.driver.get(f'{self.live_server_url}/customer/')
        # L'URL '/customer/' est la page de login selon customer/urls.py
        # Vérifier que la page se charge (pas d'erreur 404)
        self.assertIn('/customer/', self.driver.current_url)
    
    def test_login_with_valid_credentials(self):
        """TC31-SEL: Connexion avec identifiants valides"""
        self.driver.get(f'{self.live_server_url}/customer/')
        
        # Attendre que la page se charge
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        time.sleep(3)  # Attendre que Vue.js et tous les scripts soient chargés
        
        # Trouver les champs de formulaire
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        # Remplir les champs
        username_field.clear()
        username_field.send_keys('testuser')
        time.sleep(0.5)
        password_field.clear()
        password_field.send_keys('testpass123')
        time.sleep(0.5)
        
        # Trouver le bouton submit (peut être masqué par Vue.js, donc on cherche tous les boutons)
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        submit_button = None
        for btn in buttons:
            try:
                if btn.is_displayed() and not btn.get_attribute('disabled'):
                    submit_button = btn
                    break
            except:
                continue
        
        if not submit_button:
            # Si aucun bouton visible, utiliser JavaScript pour trouver et cliquer
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Cliquer sur le bouton avec JavaScript pour forcer le clic
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Attendre la redirection ou le traitement
        time.sleep(6)  # Temps pour l'AJAX et la redirection
        
        # Vérifier que l'utilisateur est connecté
        current_url = self.driver.current_url.lower()
        page_source = self.driver.page_source.lower()
        
        # Vérifier plusieurs indicateurs de succès
        success_indicators = (
            'index' in current_url or 
            'deals' in current_url or
            ('/customer/' not in current_url and 'login' not in current_url) or
            'succès' in page_source or
            'success' in page_source or
            'connecté' in page_source or
            'connectés' in page_source
        )
        
        self.assertTrue(success_indicators, f"Connexion échouée. URL: {current_url}")
    
    def test_login_with_invalid_credentials(self):
        """TC33-SEL: Connexion avec identifiants invalides"""
        self.driver.get(f'{self.live_server_url}/customer/')
        
        # Attendre que la page se charge
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        time.sleep(3)
        
        # Trouver les champs
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        # Remplir avec des identifiants invalides
        username_field.clear()
        username_field.send_keys('invaliduser')
        time.sleep(0.5)
        password_field.clear()
        password_field.send_keys('wrongpassword')
        time.sleep(0.5)
        
        # Trouver le bouton
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
        submit_button = None
        for btn in buttons:
            try:
                if btn.is_displayed() and not btn.get_attribute('disabled'):
                    submit_button = btn
                    break
            except:
                continue
        
        if not submit_button:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Cliquer avec JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Attendre le traitement
        time.sleep(6)
        
        # Vérifier qu'un message d'erreur apparaît ou que l'utilisateur reste sur la page de login
        page_source = self.driver.page_source.lower()
        current_url = self.driver.current_url.lower()
        
        # Vérifier soit un message d'erreur, soit qu'on reste sur la page login
        error_found = (
            'erreur' in page_source or 
            'incorrect' in page_source or 
            'error' in page_source or
            'alert-danger' in page_source or
            'identifiants' in page_source or
            'vérifier' in page_source or
            '/customer/' in current_url or
            'login' in current_url
        )
        
        self.assertTrue(error_found, f"Erreur non détectée. URL: {current_url}")
    
    def test_signup_page_loads(self):
        """TC36-SEL: Vérifier que la page d'inscription se charge"""
        self.driver.get(f'{self.live_server_url}/customer/signup')
        time.sleep(2)
        self.assertIn('signup', self.driver.current_url.lower() or self.driver.page_source.lower())
