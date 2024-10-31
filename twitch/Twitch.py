import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Navigation vers Twitch

def scrape_twitch(driver):

    driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")
    time.sleep(1)

    # card correspond à l'ensemble des informations textuelles dans la carte de jeu

    game_title= []
    viewers= []
    tags= []

    for i in range(0, 10):  # Remplacer 10 par le nombre maximum de cartes que tu souhaites scraper
        try:
            # Attendre que l'élément avec un style 'order: i;' soit présent
            card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(@style, 'order: {i};') and not(@id='directory-rectangle')]"))
            )

            # Extraire le titre du jeu
            game_title.append(card.find_element(By.XPATH, f"//a[contains(@data-a-target, 'card-{i}')]//h2").text)
            
            # Extraire le nombre de spectateurs
            viewers.append(card.find_element(By.XPATH, f"//p//a[contains(@data-a-target, 'card-{i}')]").text)

            # Extraire le lien vers la catégorie du jeu
            tag_elements = card.find_elements(By.XPATH, ".//button[@aria-label]//span")
            tags.append([tag.text for tag in tag_elements])

        except Exception as e:
            print(f'Erreur de récupération à la position {i}.')

    # On range toutes les informations dans une dataframe

    data_twitch= pd.DataFrame(list(zip(game_title, viewers, tags)), columns=["Game", "Viewers", "Tags"]) #Dataframe final

    return data_twitch