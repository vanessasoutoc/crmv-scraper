import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType
from datetime import datetime
import time
import json

class CRMVScraper:
    def __init__(self):
        self.base_url = "https://siscad.cfmv.gov.br"
        self.session = requests.Session()
        self.driver = None
    
    def _get_recaptcha_token(self):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--remote-debugging-port=9222')
            
            # Chrome binary location for Docker
            options.binary_location = "/usr/bin/google-chrome"
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(f"{self.base_url}/paginas/busca")

            time.sleep(3)  # Tempo para o script executar

            # Aguardar o token ser inserido no campo
            wait = WebDriverWait(self.driver, 10)
            token_field = wait.until(
                EC.presence_of_element_located((By.NAME, "g-recaptcha-response"))
            )

            # Aguardar o token ter valor
            wait.until(lambda d: token_field.get_attribute("value") != "")

            # Pegar o token
            token = token_field.get_attribute("value")
            return token
        except Exception as e:
            print(f"Error getting reCAPTCHA token: {str(e)}")
            if self.driver:
                self.driver.quit()
            return None
        finally:
            if self.driver:
                self.driver.quit()
    
    def search_crmv(self, crmv_number, state):
        try:
            # Obter token do reCAPTCHA
            recaptcha_token = self._get_recaptcha_token()

            if not recaptcha_token:
                return {"error": "Failed to get reCAPTCHA token"}

            search_url = f"{self.base_url}/pf/consultaInscricao/{crmv_number}/3/2/{state}/{recaptcha_token}?={datetime.now()}"
            
            response = self.session.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract veterinarian data from the response
            result = self._parse_result(soup)
            return result
            
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Parsing failed: {str(e)}"}
    
    def _parse_result(self, soup):
        results = json.loads(soup.text)
        return results
    
    def __del__(self):
        if self.driver:
            self.driver.quit()