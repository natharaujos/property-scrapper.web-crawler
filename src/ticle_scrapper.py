from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.request import urlopen
from bs4 import BeautifulSoup
from interfaces.property import Property

class TicleScrapper():
    def __init__(self):
        self.driver = webdriver.Chrome() 
        self.driver.get("https://www.ticleimoveis.com.br/index")
        self.driver.set_window_size(1920, 1080)
        self.wait = WebDriverWait(self.driver, 20)
        self.link = "https://www.ticleimoveis.com.br/index"

    async def find_elements_to_interact(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > mat-sidenav-container > mat-sidenav-content > mat-toolbar > div.ng-star-inserted > button:nth-child(3)"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > mat-sidenav-container > mat-sidenav-content > busca-resultado > div > form > div > div:nth-child(3) > div > mat-form-field > div > div.mat-form-field-flex"))).click()

        lavras_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'LAVRAS')]")))
        lavras_option.click()
    
    def filter_data(self, data_list: list):
        properties_filtered = []
        
        for data in data_list:
            parts = data.split("R$")
            name = parts[0].strip()
            parts2 = parts[1].split(",", 1)
            value = "R$" + parts2[0].strip()
            description: str = parts2[1].strip()
            description_formated = description.replace("00", "").replace("Mais detalhes", "")
            property = Property(name, value, description_formated, self.link)
            properties_filtered.append(property)
            
        return properties_filtered

    async def execute_scrapping(self):
        finded_elements = []
        while True:  
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.position-card')))
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('.position-card')  
            
            for element in elements:
                # only gets residencial e available elements
                if "Sob Consulta" not in element.text and "Comercial" not in element.text:
                    finded_elements.append(element.text)  
                    
            try:
                next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > app-root > mat-sidenav-container > mat-sidenav-content > busca-resultado > div > div:nth-child(6) > mat-paginator > div > div > div.mat-paginator-range-actions > button.mat-paginator-navigation-next.mat-icon-button.mat-button-base")))
                self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
                next_button.click()
                
            except TimeoutException:
                break  
            
            except NoSuchElementException:
                break  

        self.driver.quit()
        filtered_datas = self.filter_data(finded_elements)
        
        for filtered_data in filtered_datas:
            print("nome", filtered_data.name)
            print("valor", filtered_data.value)
            print("descricao", filtered_data.description)
        
        return filtered_datas