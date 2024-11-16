import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_twitch(driver):

    driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")
    time.sleep(1)

    game_title= []
    viewers= []
    tags= []

    for i in range(0, 10):
        try:

            card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(@style, 'order: {i};') and not(@id='directory-rectangle')]"))
            )

            game_title.append(card.find_element(By.XPATH, f"//a[contains(@data-a-target, 'card-{i}')]//h2").text)
            
            viewers.append(card.find_element(By.XPATH, f"//p//a[contains(@data-a-target, 'card-{i}')]").text)

            tag_elements = card.find_elements(By.XPATH, ".//button[@aria-label]//span")
            tags.append([tag.text for tag in tag_elements])

        except Exception as e:
            print(f'Erreur de récupération à la position {i}.')

    data_twitch= pd.DataFrame(list(zip(game_title, viewers, tags)), columns=["Game", "Viewers", "Tags"])

    return data_twitch