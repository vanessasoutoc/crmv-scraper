import pytest
import requests_mock
import requests
from crmv_scraper import CRMVScraper

@pytest.fixture
def scraper():
    return CRMVScraper()

def test_search_crmv_success(scraper):
    mock_json = '{"type": "sucess", "data": [{"id_pf_inscricao": 259054, "pf_inscricao": "02655", "pf_classe": "VP", "pf_uf": "MG", "nome": "CLAUDIO BARRETO", "nome_social": null, "atuante": true, "dt_inscricao": "1984-12-08T00:00:00+00:00", "cpf": "42995973620"}], "haveMoreThanLimitConsultaRegisters": false}'
    
    with requests_mock.Mocker() as m:
        # Mock both the initial page and the search URL
        m.get(f"{scraper.base_url}/paginas/busca", text="<html></html>")
        m.get(requests_mock.ANY, text=mock_json)
        
        # Mock the reCAPTCHA token method to avoid Selenium
        scraper._get_recaptcha_token = lambda: "mock_token"
        
        result = scraper.search_crmv("02655", "MG")
        
        assert result["data"] is not None
        assert result["type"] == "sucess"

def test_search_crmv_request_error(scraper):
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, exc=requests.exceptions.ConnectTimeout)
        
        # Mock the reCAPTCHA token method to avoid Selenium
        scraper._get_recaptcha_token = lambda: "mock_token"
        
        result = scraper.search_crmv("12345", "MG")
        
        assert 'error' in result
        assert 'Request failed' in result['error']